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
    if not user.year_in:
        my_bot.send_message(chat_id, 'Выберите дату заезда:', reply_markup=types.ReplyKeyboardRemove())
    else:
        my_bot.send_message(chat_id, 'Выберите дату выезда:', reply_markup=types.ReplyKeyboardRemove())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    years = [2023, 2024]
    if user.year_in:
        index = years.index(user.year_in)
        if user.flag_last_day_month and user.flag_last_month:
            index += 1
        years = years[index:]
        amount_days = monthrange(user.year_in, user.month_in)[1]
        if amount_days - user.day_in >= 27:
            years = years[:years.index(user.year_in) + 1]

    keyboard.add(*[types.InlineKeyboardButton(year) for year in years])
    years = my_bot.send_message(chat_id, 'Выберите год', reply_markup=keyboard)
    my_bot.register_next_step_handler(years, get_month)


def get_month(message) -> None:
    """
    Создает клавиатуру месяцев и предлагает выбор
    """
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    months = ["Января", "Февраля", "Марта",
              "Апреля", "Мая", "Июня",
              "Июля", "Августа", "Сентября",
              "Октября", "Ноября", "Декабря"]
    try:
        if not user.year_in or not user.year_out and user.year_in:
            if message.text == '/help' or message.text == '/start':
                raise FileNotFoundError
            year = int(message.text)
            year_now = datetime.datetime.now().year
            if year_now > year or year > year_now + 2:
                raise ValueError
    except ValueError:
        my_bot.send_message(chat_id, 'Что-то не так с годом.\n '
                                     'Выберите из предложенных или введите год в диапазоне 2022-2023')
        my_bot.send_message(chat_id, 'Для возврата к началу /help')
        get_year(message)
    except FileNotFoundError:
        user_help(message)
    else:
        if not user.year_in or not user.year_out and user.year_in:
            if not user.year_in:
                user.year_in = int(message.text)  # Сохраняем год даты въезда
            else:
                user.year_out = int(message.text)  # Сохраняем год даты въезда

        if not user.year_out:
            year = user.year_in
        else:
            year = user.year_out

        year_now = datetime.datetime.now().year
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if year == year_now and not user.month_in:
            month_now = datetime.datetime.now().month - 1
            months = months[month_now:]
        elif user.month_in and year == year_now:
            index = user.month_in - 1
            if user.flag_last_day_month:
                index += 1
            months = months[index:]
        if user.month_in:
            amount_days = monthrange(year, user.month_in)[1]
            if amount_days - user.day_in >= 27:
                months = months[user.month_in - 1:user.month_in]
            else:
                if len(months) != 1:
                    months = months[:user.month_in % 12 + 1]
                    user.day_out = 27 - (amount_days - user.day_in)

        keyboard.add(*[types.InlineKeyboardButton(month) for month in months])
        months = my_bot.send_message(chat_id, 'Выберите месяц', reply_markup=keyboard)
        my_bot.register_next_step_handler(months, get_day)


def get_day(message) -> None:
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    try:
        if not user.month_in or not user.month_out and user.month_in:
            if message.text == '/help' or message.text == '/start':
                raise FileNotFoundError
            datetime.datetime.strptime(message.text, '%B')
    except ValueError:
        my_bot.send_message(chat_id, 'Проблемы с месяцем, выберите из предложенных.'
                                     ' Либо введите в формате: (Января, Февраля, Марта и т.п.)')
        my_bot.send_message(chat_id, 'Для возврата к началу /help')
        get_month(message)
    except FileNotFoundError:
        user_help(message)
    else:
        if not user.month_in or user.year_out and user.month_in:
            if not user.month_in:
                user.month_in = int(datetime.datetime.strptime(message.text, '%B').month)
                if message.text == 'Декабрь':
                    user.flag_last_month = True
            else:
                user.month_out = int(datetime.datetime.strptime(message.text, '%B').month)

        if user.day_in:
            year = user.year_out
            user_month = user.month_out
        elif not user.day_in:
            year = user.year_in
            user_month = user.month_in
        month_now = datetime.datetime.now().month
        year_now = datetime.datetime.now().year
        amount_days = monthrange(year, user_month)[1]
        days_list = list(range(1, amount_days + 1))
        day_now = datetime.datetime.now().day - 1
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if not user.day_in:
            if month_now == user_month and user.year_in == year_now:
                days_list = days_list[day_now:]
        elif user.day_in and not user.flag_last_day_month:
            input_month = int(datetime.datetime.strptime(message.text, '%B').month)
            if user.month_in == input_month:  # Проверяем если месяц въезда равен введенному месяцу выезда
                index = user.day_in
                days_list = days_list[index:]
        if user.day_out:
            days_list = days_list[:user.day_out]
        if len(days_list) <= 12:
            keyboard.add(*[types.InlineKeyboardButton(day) for day in days_list])
        else:
            keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[:len(days_list) // 3]])
            keyboard.row(*[types.InlineKeyboardButton(day) for day in
                           days_list[len(days_list) // 3:len(days_list) - len(days_list) // 3]])
            keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[len(days_list) - len(days_list) // 3:]])
        days = my_bot.send_message(chat_id, 'Выберите день', reply_markup=keyboard)
        my_bot.register_next_step_handler(days, confirm_date)


def confirm_date(message) -> None:
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    try:
        if not user.day_in or not user.day_out and user.day_in:
            if message.text == '/help' or message.text == '/start':
                raise FileNotFoundError
            num_day = int(message.text)
            if not user.day_in:
                last_day_month = monthrange(user.year_in, user.month_in)[1]
            elif user.day_in:
                last_day_month = monthrange(user.year_out, user.month_out)[1]
            if num_day > last_day_month:
                raise ValueError
    except ValueError:
        my_bot.send_message(chat_id,
                            'Какой-то странный день, выберите из предложенных, либо введите верное число',
                            reply_markup=types.ReplyKeyboardRemove())
        my_bot.send_message(chat_id, 'Для возврата к началу /help')
        get_day(message)
    except FileNotFoundError:
        user_help(message)
    else:
        if not user.day_in:
            num_day = int(message.text)
            last_day_month = monthrange(user.year_in, user.month_in)[1]
            if last_day_month == num_day:
                user.flag_last_day_month = True
        if not user.day_in:
            user.day_in = int(message.text)
        else:
            user.day_out = int(message.text)
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_date')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no_date')
        keyboard.add(key_yes, key_no)
        if not user.day_out:
            my_bot.send_message(chat_id, f'Дата заезда {user.day_in}.{user.month_in}.{user.year_in}?', reply_markup=keyboard)
        else:
            my_bot.send_message(chat_id, f'Дата выезда {user.day_out}.{user.month_out}.{user.year_out}?', reply_markup=keyboard)


locale.setlocale(
    category=locale.LC_ALL,
    locale="ru_RU.UTF-8"
)
