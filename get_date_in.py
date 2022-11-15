from telebot import types

from get_date import get_year, get_month, get_day

from my_bot import my_bot
from user_class import User
from datetime import datetime

def get_date_in(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    keyboard = get_year()
    my_bot.send_message(chat_id, 'Выберите год', reply_markup=keyboard)
    # keyboard = get_month()
    # my_bot.send_message(chat_id, 'Выберите год', reply_markup=keyboard)


@my_bot.callback_query_handler(func=lambda call: True)
def callback_date(call):
    chat_id = call.message.chat.id
    user = User.get_user(chat_id)
    my_bot.edit_message_reply_markup(chat_id, message_id=call.message.id, reply_markup=None)
    if not user.check_in:
        user.check_in = call.data
    else:
        user.check_in += f'-{call.data}'

import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)

