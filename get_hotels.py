import re
from typing import List, Dict

from telebot import types

from api_request_hotels import api_request_hotel
from get_photos import get_photo
from my_bot import my_bot
from output_hotels_list import output_hotels
from user_class import User


def get_hotels(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    user.dict_photos.clear()
    user.hotels_list.clear()
    msg = my_bot.send_message(chat_id, 'Загружаю данные...')
    api_hotels_list = api_request_hotel(message)[:]
    user.hotels_list = create_hotels_list(chat_id, api_hotels_list)
    if user.need_to_get_photo:
        get_photo(chat_id)
    output_hotels(msg)


def create_hotels_list(chat_id, hotels_list_api: List[Dict]) -> List[str]:
    """
    Функция создает список строк с данными отелей
    :param chat_id: Id пользователя для открытия его класса
    :param hotels_list_api: Список отелей со всеми данными
    :return: Список отелей с нужными данными
    """
    user = User.get_user(chat_id)
    hotels_list = []
    for hotel in hotels_list_api:
        name_hotel = hotel['name']
        if not 'streetAddress' in hotel['address']:
            continue
        address = hotel['address']["streetAddress"]
        distance_miles = hotel['landmarks'][0]['distance']
        miles = re.search(r'\S*', distance_miles).group()
        distance_from_center = round(float(miles) * 1.7, 1)
        price_night = hotel['ratePlan']['price']['current']
        full_price_str = hotel['ratePlan']['price']['fullyBundledPricePerStay']
        full_price = re.search(r'.*RUB', full_price_str).group()
        hotels_list.append(f'Название отеля: {name_hotel}\n'
                           f'Адрес: {address}\n'
                           f'Расстояние от центра: {distance_from_center} км\n'
                           f'Стоимость за ночь: {price_night}\n'
                           f'Полная стоимость: {full_price[6:]}')
        if user.need_to_get_photo:
            user.dict_photos[str(hotel['id'])] = []
    return hotels_list
