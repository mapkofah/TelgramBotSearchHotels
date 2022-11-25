import datetime

from telebot import types
import locale

from api_request_hotels import api_request_hotel
from data_town import data_town
from get_date import get_year
from get_hotels import get_hotels
from my_bot import my_bot
from need_photos import amount_photos
from user_class import User
from get_town import get_towns_in_api
from amount_hotels_page import amount_hotels_page


@my_bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    """
    Обработка сообщения с Inline кнопки
    :param call: данные с кнопки
    """
    chat_id = call.message.chat.id
    user = User.get_user(chat_id)
    if call.data == 'back':
        my_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите название города: ")
        my_bot.register_next_step_handler(call.message, get_towns_in_api)
    elif user.user_command != '/history' and not user.city:
        user.city = call.data
        user.city_gaiaId = user.towns_dict.get(call.data)
        destinationId = data_town(call.data, user.city_gaiaId)
        user.city_id = destinationId
        my_bot.delete_message(call.message.chat.id, call.message.message_id)
        get_year(call.message)
    elif call.data == 'yes_date':
        if not user.flag_check_in:
            user.check_in.reverse()
            user.flag_check_in = True
            my_bot.delete_message(call.message.chat.id, call.message.message_id)
            get_year(call.message)
        else:
            user.check_out.reverse()
            user.check_in = '-'.join(user.check_in)
            if len(user.check_out) == 3:
                user.check_out = '-'.join(user.check_out)
            user.check_in = str(datetime.datetime.strptime(user.check_in, '%Y-%B-%d'))[:10]
            user.check_out = str(datetime.datetime.strptime(user.check_out, '%Y-%B-%d'))[:10]
            my_bot.delete_message(call.message.chat.id, call.message.message_id)
            my_bot.send_message(chat_id, f'Въезд {user.check_in} \nВыезд {user.check_out}', reply_markup=types.ReplyKeyboardRemove())
            amount_hotels_page(call.message)

    elif call.data == 'no_date':
        my_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text="Введите дату еще раз: ")
        if not user.flag_check_in:
            user.check_in = []
        else:
            user.check_out = []
        get_year(call.message)
    elif call.data == 'yes_photos':
        user.need_to_get_photo = True
        my_bot.send_message(chat_id, 'Введите количество фотографий каждого отеля. (максимум 5)')
        my_bot.register_next_step_handler(call.message, amount_photos)
    elif call.data == 'no_photos':
        get_hotels(call.message)

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)
