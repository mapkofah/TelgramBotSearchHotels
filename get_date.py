from telebot import types


def get_year():
    keyboard = types.InlineKeyboardMarkup()
    years = ['2022', '2023']
    for year in years:
        key = types.InlineKeyboardButton(text=year, callback_data=year)
        keyboard.add(key)
    return keyboard


def get_month():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.InlineKeyboardButton(month) for month in ["Январь", "Февраль", "Март",
                                                                   "Апрель", "Май", "Июнь",
                                                                   "Июль", "Август", "Сентябрь",
                                                                   "Октябрь", "Ноябрь", "Декабрь"]])


def get_day(month):
    pass
