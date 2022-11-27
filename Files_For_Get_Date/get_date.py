import locale
from telebot import types
from calendar import monthrange

from Bot_Commands.help import user_help
from Bot_Files.my_bot import my_bot
from Bot_Files.user_class import User
import datetime


def get_year(message) -> None:
    """
    Создает клавиатуру и предлагает выбор года
    """
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    if not user.flag_check_in:
        my_bot.send_message(chat_id, 'Выберите дату заезда:', reply_markup=types.ReplyKeyboardRemove())
    else:
        my_bot.send_message(chat_id, 'Выберите дату выезда:', reply_markup=types.ReplyKeyboardRemove())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    years = ['2022', '2023']
    if user.flag_check_in:
        index = years.index(user.check_in[0])
        if user.flag_last_day_month and user.flag_last_month:
            index += 1
        years = years[index:]
    keyboard.add(*[types.InlineKeyboardButton(year) for year in years])
    years = my_bot.send_message(chat_id, 'Выберите год', reply_markup=keyboard)
    my_bot.register_next_step_handler(years, get_month)


def get_month(message) -> None:
    """
    Создает клавиатуру месяцев и предлагает выбор
    """
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    months = ["Январь", "Февраль", "Март",
              "Апрель", "Май", "Июнь",
              "Июль", "Август", "Сентябрь",
              "Октябрь", "Ноябрь", "Декабрь"]
    try:
        if len(user.check_in) == 0 and not user.flag_check_in \
                or len(user.check_out) == 0 and user.flag_check_in:
            if message.text == '/help' or message.text == '/start':
                raise FileNotFoundError
            year = int(message.text)
            year_now = datetime.datetime.now().year
            if year_now > year or year > year_now + 2:
                raise ValueError
    except ValueError:
        my_bot.send_message(chat_id, 'Что-то не так с годом.\n '
                                     'Выберите из предложенных или введите год в диапазоне 2022-2024')
        my_bot.send_message(chat_id, 'Для возврата к началу /help')
        get_year(message)
    except FileNotFoundError:
        user_help(message)
    else:
        if len(user.check_in) == 0 and not user.flag_check_in \
                or len(user.check_out) == 0 and user.flag_check_in:
            if not user.flag_check_in:
                user.check_in = []
                user.check_in.append(message.text)
            else:
                user.check_out = []
                user.check_out.append(message.text)
            year = message.text
        elif user.flag_check_in:
            year = user.check_out[0]
        elif not user.flag_check_in:
            year = user.check_in[0]
        year_now = str(datetime.datetime.now().year)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if year == year_now and not user.flag_check_in:
            month_now = datetime.datetime.now().month - 1
            months = months[month_now:]
        elif user.flag_check_in:
            index = months.index(user.check_in[1])
            if user.flag_last_day_month:
                index += 1
            months = months[index:]
        keyboard.add(*[types.InlineKeyboardButton(month) for month in months])
        months = my_bot.send_message(chat_id, 'Выберите месяц', reply_markup=keyboard)
        my_bot.register_next_step_handler(months, get_day)


def get_day(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    try:
        if len(user.check_in) == 1 and not user.flag_check_in \
                or len(user.check_out) == 1 and user.flag_check_in:
            datetime.datetime.strptime(message.text, '%B')
        if message.text == '/help' or message.text == '/start':
            raise FileNotFoundError
    except ValueError:
        my_bot.send_message(chat_id, 'Проблемы с месяцем, выберите из предложенных.'
                                     ' Либо введите в формате: (Январь, Февраль, Март и т.п.)')
        my_bot.send_message(chat_id, 'Для возврата к началу /help')
        get_month(message)
    except FileNotFoundError:
        user_help(message)
    else:
        if len(user.check_in) == 1 and not user.flag_check_in \
                or len(user.check_out) == 1 and user.flag_check_in:
            if not user.flag_check_in:
                user.check_in.insert(0, message.text)
            else:
                user.check_out.insert(0, message.text)
            if message.text == 'Февраль':
                year = int(user.check_in[1])
            else:
                if message.text == 'Декабрь':
                    user.flag_last_month = True
        if user.flag_check_in:
            year = int(user.check_out[1])
            user_month = user.check_out[0]
        elif not user.flag_check_in:
            year = int(user.check_in[1])
            user_month = user.check_in[0]
        month_now = datetime.datetime.now().month
        num_month = datetime.datetime.strptime(user_month, "%B").month
        amount_days = monthrange(year, num_month)[1]
        days_list = list(range(1, amount_days + 1))
        day_now = datetime.datetime.now().day - 1
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if not user.flag_check_in:
            if month_now == num_month:
                days_list = days_list[day_now:]
        elif user.flag_check_in and not user.flag_last_day_month:
            index = int(user.check_in[2])
            days_list = days_list[index:]
        if len(days_list) <= 12:
            keyboard.add(*[types.InlineKeyboardButton(day) for day in days_list])
        else:
            keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[:len(days_list) // 3]])
            keyboard.row(*[types.InlineKeyboardButton(day) for day in
                           days_list[len(days_list) // 3:len(days_list) - len(days_list) // 3]])
            keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[len(days_list) - len(days_list) // 3:]])
        days = my_bot.send_message(chat_id, 'Выберите день', reply_markup=keyboard)
        my_bot.register_next_step_handler(days, confirm_date)


def confirm_date(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    try:
        if len(user.check_in) == 2 and not user.flag_check_in \
                or len(user.check_out) == 2 and user.flag_check_in:
            num_day = int(message.text)
            if not user.flag_check_in:
                num_month = datetime.datetime.strptime(user.check_in[0], "%B").month
                year = int(user.check_in[1])
                last_day_month = monthrange(year, num_month)[1]
            elif user.flag_check_in:
                num_month = datetime.datetime.strptime(user.check_out[0], "%B").month
                year = int(user.check_out[1])
                last_day_month = monthrange(year, num_month)[1]
            if num_day > last_day_month:
                raise ValueError
        if message.text == '/help' or message.text == '/start':
            raise FileNotFoundError
    except ValueError:
        my_bot.send_message(chat_id,
                            'Какой-то странный день, выберите из предложенных, либо введите верное число',
                            reply_markup=types.ReplyKeyboardRemove())
        my_bot.send_message(chat_id, 'Для возврата к началу /help')
        get_day(message)
    except FileNotFoundError:
        user_help(message)
    else:
        if not user.flag_check_in:
            num_day = int(message.text)
            num_month = datetime.datetime.strptime(user.check_in[0], "%B").month
            year = int(user.check_in[1])
            last_day_month = monthrange(year, num_month)[1]
        if last_day_month == num_day:
            user.flag_last_day_month = True
        if len(message.text) == 1:
            if not user.flag_check_in:
                user.check_in.insert(0, f'0{message.text}')
            else:
                user.check_out.insert(0, f'0{message.text}')
        else:
            if not user.flag_check_in:
                user.check_in.insert(0, message.text)
            else:
                user.check_out.insert(0, message.text)
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_date')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no_date')
        keyboard.add(key_yes, key_no)
        if not user.flag_check_in:
            my_bot.send_message(chat_id, f'Дата заезда {"-".join(user.check_in)}?', reply_markup=keyboard)
        else:
            my_bot.send_message(chat_id, f'Дата выезда {"-".join(user.check_out)}?', reply_markup=keyboard)


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)