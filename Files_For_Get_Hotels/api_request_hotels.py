import json
import re

import requests
from Bot_Files.user_class import User
from History_database.enter_data import enter_hotels_names


def api_request_hotels(chat_id) -> None:
    """
    Функция получения отелей и их данных с API Hotels.com
    """
    user = User.get_user(chat_id)
    price_range = {}
    if user.user_command == '/bestdeal':
        sortOrder = 'DISTANCE'
        price_range = {"price": {"max": user.price_range, "min": 1}}
    else:
        sortOrder = 'PRICE_LOW_TO_HIGH'

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": user.city_id},
        "checkInDate": {
            "day": user.day_in,
            "month": user.month_in,
            "year": user.year_in
        },
        "checkOutDate": {
            "day": user.day_out,
            "month": user.month_out,
            "year": user.year_out
        },
        "rooms": [{"adults": 1}],
        "resultsStartingIndex": user.page_num,
        "resultsSize": user.page_size,
        "sort": sortOrder,
        "filters": price_range
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "1796f32a87msh6ff0e54218bd17cp132c92jsnec17a594ba8d",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    data_hotels = json.loads(response.text)
    user.hotels_names.clear()

    for hotel in data_hotels['data']['propertySearch']['properties']:
        user.hotels_dict[hotel['id']] = {}
        hotel_dict = user.hotels_dict[hotel['id']]
        hotel_dict['name'] = hotel['name']
        user.hotels_names.append(hotel['name'])
        hotel_dict['distance'] = float(hotel['destinationInfo']['distanceFromDestination']['value'])
        if user.user_command == '/bestdeal' and hotel_dict['distance'] > user.distance_range:
            user.hotels_dict.pop(hotel['id'])
            break
        hotel_dict['price_night'] = round(float(hotel['price']['lead']['amount']) * 62, 2)
        hotel_dict['total_price'] = (int(''.join(
            re.findall(r'\d+', (hotel['price']['displayMessages'][1]['lineItems'][0]['value'])))) * 62)

    if not user.page_num in user.list_page_nums:
        user.list_page_nums.append(user.page_num)
        enter_hotels_names(chat_id)
