import time

from telebot import types
from Bot_Files.my_bot import my_bot
from Bot_Files.user_class import User
from Files_For_Get_Town.api_request_towns import api_request_towns


def get_town(message) -> None:
    chat_id = message.chat.id
    user = User.get_user(message.chat.id)
    user.user_command = message.text
    tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))  # Конвертация даты в читабельный вид
    user.date_message = tconv(message.date)  # Время ввода команды
    my_bot.send_message(chat_id, 'Введите название города: ')
    my_bot.register_next_step_handler(message, get_towns_in_api)


def get_towns_in_api(message) -> None:
    name_city = message.text
    chat_id = message.chat.id
    user = User.get_user(message.chat.id)
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
