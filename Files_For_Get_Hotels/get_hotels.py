from Bot_Files.my_bot import my_bot
from Files_For_Get_Hotels.api_request_data_hotel import api_request_data_hotel
from Files_For_Get_Hotels.api_request_hotels import api_request_hotels_id
from Files_For_Get_Hotels.output_hotels_list import output_hotels
from Bot_Files.user_class import User


def get_hotels(message) -> None:
    """
    Функция получает словарь с данными отелей
    """
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    user.hotels_dict.clear()
    my_bot.send_message(chat_id, 'Загружаю данные...')
    api_request_hotels_id(chat_id)
    api_request_data_hotel(chat_id)
    output_hotels(message)

