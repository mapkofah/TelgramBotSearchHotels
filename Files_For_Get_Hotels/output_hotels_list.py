from telebot import types

from Bot_Commands.help import user_help
from Bot_Files.my_bot import my_bot
from Bot_Files.user_class import User


def output_hotels(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    keyboard = types.InlineKeyboardMarkup()
    next_page = types.InlineKeyboardButton('Следующая страница', callback_data='next_page')
    prev_page = types.InlineKeyboardButton('Предыдущая страница', callback_data='prev_page')
    home_page = types.InlineKeyboardButton('Вернуться на первую', callback_data='home_page')
    keyboard.add(next_page)
    if user.page_num != 0:
        keyboard.add(prev_page)
        keyboard.add(home_page)
    try:
        for hotel_id in user.hotels_dict.keys():
            hotel_dict = user.hotels_dict[hotel_id]
            if hotel_dict.get('photo'):
                my_bot.send_media_group(chat_id, hotel_dict['photo'])
            else:
                my_bot.send_message(chat_id, hotel_dict['output_string'])
        my_bot.send_message(chat_id, 'Выберите действие', reply_markup=keyboard)
        if message.text == '/help' or message.text == '/start':
            raise FileNotFoundError
    except FileNotFoundError:
        user_help(message)
