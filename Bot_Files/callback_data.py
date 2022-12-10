from telebot import types
import locale

from Bot_Commands.help import user_help
from Files_For_Get_Date.get_date import get_year
from Files_For_Get_Hotels.get_hotels import get_hotels
from Bot_Files.my_bot import my_bot
from Files_For_Get_Photos.need_photos import amount_photos
from Bot_Files.user_class import User
from Files_For_Get_Range.get_price_range import price_range
from Files_For_Get_Town.get_town import get_towns_in_api
from Files_For_Get_Hotels.amount_hotels_page import amount_hotels_page


@my_bot.callback_query_handler(func=lambda call: True)
def callback_data(call) -> None:
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
        user.city_id = user.towns_dict.get(call.data)
        my_bot.delete_message(chat_id, call.message.message_id)
        get_year(call.message)
    elif call.data == 'yes_date':
        if not user.day_out:
            my_bot.delete_message(chat_id, call.message.message_id)
            get_year(call.message)
        else:
            my_bot.delete_message(chat_id, call.message.message_id)
            my_bot.send_message(chat_id, f'Въезд {user.day_in}.{user.month_in}.{user.year_in} \nВыезд {user.day_out}.{user.month_out}.{user.year_out}', reply_markup=types.ReplyKeyboardRemove())
            if user.user_command == '/bestdeal':
                price_range(call.message)
            else:
                amount_hotels_page(call.message)
    elif call.data == 'no_date':
        my_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text="Введите дату еще раз: ")
        if not user.day_out:
            user.year_in, user.month_in, user.day_in = None, None, None
        else:
            user.year_out, user.month_out, user.day_out = None, None, None
        get_year(call.message)
    elif call.data == 'yes_photos':
        user.need_to_get_photo = True
        my_bot.send_message(chat_id, 'Введите количество фотографий каждого отеля. (максимум 5)')
        my_bot.register_next_step_handler(call.message, amount_photos)
    elif call.data == 'no_photos':
        get_hotels(call.message)
    elif call.data == 'next_page':
        my_bot.delete_message(chat_id, call.message.message_id)
        user.page_num += 1
        get_hotels(call.message)
    elif call.data == 'prev_page':
        my_bot.delete_message(chat_id, call.message.message_id)
        user.page_num -= 1
        get_hotels(call.message)
    elif call.data == 'home_page':
        my_bot.delete_message(chat_id, call.message.message_id)
        user.page_num = 0
        get_hotels(call.message)
    elif call.data == 'yes_range':
        price_range(call.message)
    elif call.data == 'no_range':
        user_help(call.message)


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)
