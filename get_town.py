from telebot import types
from data_town import data_town
from get_date_in import get_date_in
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
    chat_id = message.from_user.id
    towns_list = api_request_towns(name_city)
    keyboard = types.InlineKeyboardMarkup()
    for item in towns_list:
        if item['type'] == 'CITY':
            town_name = item['regionNames']["fullName"]
            gaiaId = item['gaiaId']
            user.towns_dict[town_name] = gaiaId
            key = types.InlineKeyboardButton(text=town_name, callback_data=town_name)
            keyboard.add(key)
    key_back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    keyboard.add(key_back)
    my_bot.send_message(chat_id, text='Выберите ваш вариант:', reply_markup=keyboard)

@my_bot.callback_query_handler(func=lambda call: True)
def callback_towns(call):
    chat_id = call.message.chat.id
    my_bot.send_message(chat_id, str(call.data))
    user = User.get_user(chat_id)
    if call.data == 'back':
        get_town(call.message)
    else:
        user.city = call.data
        user.city_gaiaId = user.towns_dict.get(call.data)
        destinationId = data_town(call.data, user.city_gaiaId)
        user.city_id = destinationId
        my_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
        # my_bot.edit_message_reply_markup(chat_id, message_id=call.message.id, reply_markup=None)
    # my_bot.answer_callback_query(chat_id)
