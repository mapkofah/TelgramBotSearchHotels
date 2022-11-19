from telebot import types

from data_town import data_town
from get_date import get_year
from my_bot import my_bot
from user_class import User
from get_town import get_towns_in_api


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
    # elif user.user_command != '/history' and not user.city:
    #     user.city = call.data
    #     user.city_gaiaId = user.towns_dict.get(call.data)
    #     destinationId = data_town(call.data, user.city_gaiaId)
    #     user.city_id = destinationId
    #     my_bot.delete_message(call.message.chat.id, call.message.message_id)
    #     get_year(call.message)
    elif call.data == 'yes_date':
        if not user.flag_check_in:
            user.check_in.reverse()
            user.flag_check_in = True
            get_year(call.message)
        else:
            user.check_out.reverse()
            my_bot.send_message(chat_id, 'Получилось получить дату вьезда и выезда', reply_markup=types.ReplyKeyboardRemove())
    elif call.data == 'no_date':
        my_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text="Введите дату еще раз: ")
        if not user.flag_check_in:
            user.check_in = []
        else:
            user.check_out = []
        get_year(call.message)


