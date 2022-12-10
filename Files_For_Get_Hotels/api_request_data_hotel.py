import json

import requests
from telebot import types

from Bot_Files.user_class import User


def api_request_data_hotel(chat_id) -> None:
    user = User.get_user(chat_id)
    for hotel_id in user.hotels_dict.keys():
        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

        payload = {
            "currency": "RUB",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "propertyId": hotel_id
        }
        headers = {
            'content-type': 'application/json',
            'X-RapidAPI-Key': '1796f32a87msh6ff0e54218bd17cp132c92jsnec17a594ba8d',
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        data_hotel = json.loads(response.text)
        hotel_dict = user.hotels_dict[hotel_id]

        hotel_dict['address'] = data_hotel['data']['propertyInfo']['summary']['location']['address']['addressLine']
        hotel_dict['output_string'] = f'Название отеля: {hotel_dict["name"]}\n' \
                                      f'Адрес: {hotel_dict["address"]}\n' \
                                      f'Расстояние от центра: {hotel_dict["distance"]} км\n' \
                                      f'Стоимость за ночь: {hotel_dict["price_night"]} руб\n' \
                                      f'Полная стоимость: {hotel_dict["total_price"]} руб'
        if user.need_to_get_photo:
            hotel_dict['photo'] = []
            index = 0
            while index != user.amount_photo:
                url_image = data_hotel['data']['propertyInfo']['propertyGallery']['images'][index]['image']['url']
                if index == 0:
                    hotel_dict['photo'].append(types.InputMediaPhoto(url_image, caption=hotel_dict['output_string']))
                else:
                    hotel_dict['photo'].append(types.InputMediaPhoto(url_image))
                index += 1
