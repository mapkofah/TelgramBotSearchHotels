import locale
from telebot import types
from calendar import monthrange
from my_bot import my_bot
from user_class import User
import datetime


def get_year(message) -> None:
    """
    Создает клавиатуру и предлагает выбор года
    """
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    years = ['2022', '2023']
    if user.flag_check_in:
        index = years.index(user.check_in)
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
    if not user.flag_check_in:
        user.check_in.append(message.text)
    else:
        user.check_out = message.text
    year_now = str(datetime.datetime.now().year)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) ### check_out сделать что бы дата была от числа check_in
    if message.text == year_now:
        month_now = datetime.datetime.now().month - 1
        months = months[month_now:]
    elif user.flag_check_in:
        index = months.index(user.check_in[1])
        months = months[index:]
    keyboard.add(*[types.InlineKeyboardButton(month) for month in months])
    months = my_bot.send_message(chat_id, 'Выберите месяц', reply_markup=keyboard)
    my_bot.register_next_step_handler(months, get_day)


def get_day(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    if not user.flag_check_in:
        user.check_in.insert(0, message.text)
    else:
        user.check_out.insert(0, message.text)
    if message.text == 'Февраль':
        year = int(user.check_in[:4])
        days_list = list(range(1, monthrange(year, 2) + 1))
    elif message.text in ['Апрель', 'Июнь', 'Сентябрь', 'Ноябрь']:
        days_list = list(range(1, 31))
    else:
        days_list = list(range(1, 32))
    month_now = datetime.datetime.now().month
    num_month = datetime.datetime.strptime(message.text, "%B").month
    day_now = datetime.datetime.now().day - 1
    if month_now == num_month:
        days_list = days_list[day_now:]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[:len(days_list) // 3]])
    keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[len(days_list) // 3:len(days_list) - len(days_list) // 3]])
    keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[len(days_list) - len(days_list) // 3:]])
    days = my_bot.send_message(chat_id, 'Выберите день', reply_markup=keyboard)
    my_bot.register_next_step_handler(days, confirm_date)


def confirm_date(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
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

