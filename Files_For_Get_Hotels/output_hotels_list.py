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
    if user.page_num != 1:
        keyboard.add(prev_page)
        keyboard.add(home_page)
    try:
        if user.need_to_get_photo:
            index = 0
            for value in user.dict_photos.values():
                my_bot.send_message(chat_id, user.hotels_list[index])
                index += 1
                my_bot.send_media_group(chat_id, value)
        else:
            for hotel in user.hotels_list:
                my_bot.send_message(chat_id, hotel)
        my_bot.send_message(chat_id,'Выберите действие', reply_markup=keyboard)
        if message.text == '/help' or message.text == '/start':
            raise FileNotFoundError
    except FileNotFoundError:
        user_help(message)


