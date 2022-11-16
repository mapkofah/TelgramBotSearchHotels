import locale
from telebot import types
from calendar import monthrange
from my_bot import my_bot
from user_class import User
from datetime import datetime


def get_year(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.InlineKeyboardButton(year) for year in ['2022', '2023']])
    years = my_bot.send_message(chat_id, 'Выберите год', reply_markup=keyboard)
    my_bot.register_next_step_handler(years, get_month)


def get_month(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    if not user.flag_check_in:
        user.check_in.append(message.text)
    else:
        user.check_out = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) ### check_out сделать что бы дата была от числа check_in
    keyboard.add(*[types.InlineKeyboardButton(month) for month in ["Январь", "Февраль", "Март",
                                                                   "Апрель", "Май", "Июнь",
                                                                   "Июль", "Август", "Сентябрь",
                                                                   "Октябрь", "Ноябрь", "Декабрь"]])
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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[:10]])
    keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[10:21]])
    keyboard.row(*[types.InlineKeyboardButton(day) for day in days_list[21:]])
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
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)

