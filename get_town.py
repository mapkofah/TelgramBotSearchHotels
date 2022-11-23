from telebot import types
from my_bot import my_bot
from user_class import User
from api_request_towns import api_request_towns


def get_town(message):
    chat_id = message.chat.id
    user = User.get_user(message.chat.id)
    user.user_command = message.text
    my_bot.send_message(chat_id, 'Введите название города: ')
    my_bot.register_next_step_handler(message, get_towns_in_api)


def get_towns_in_api(message):
    name_city = message.text
    user = User.get_user(message.chat.id)
    chat_id = message.chat.id
    towns_list = api_request_towns(name_city)
    keyboard = types.InlineKeyboardMarkup()
    flag = True
    for item in towns_list:
        if item['type'] == 'CITY':
            town_name = item['regionNames']["fullName"]
            gaiaId = item['gaiaId']
            user.towns_dict[town_name] = gaiaId
            key = types.InlineKeyboardButton(text=town_name, callback_data=town_name)
            keyboard.add(key)
            flag = False
    if flag:
        msg = my_bot.send_message(chat_id, 'Город не найден, попробуйте еще раз.')
        get_town(msg)
    else:
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        keyboard.add(key_back)
        my_bot.send_message(chat_id, text='Выберите ваш вариант:', reply_markup=keyboard)

