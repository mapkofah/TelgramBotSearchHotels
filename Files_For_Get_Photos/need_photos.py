from telebot import types

from Files_For_Get_Hotels.get_hotels import get_hotels
from Bot_Files.my_bot import my_bot
from Bot_Files.user_class import User


def need_photo(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_photos')
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no_photos')
    keyboard.add(key_yes, key_no)
    my_bot.send_message(chat_id, 'Загрузить фотографии отелей?', reply_markup=keyboard)


def amount_photos(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    try:
        amount = int(message.text)
        if amount > 5 or amount < 1:
            raise OverflowError
    except:
        msg = my_bot.send_message(chat_id, 'Ошибочно введено количество фотографий, введите число до 5')
        my_bot.register_next_step_handler(msg, amount_photos)
    else:
        user.amount_photo = int(message.text)
        get_hotels(message)