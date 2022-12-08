import json
import re

import requests
from Bot_Files.user_class import User


def api_request_hotels_id(chat_id) -> None:
    """
    Функция получения hotel id с API Hotels.com
    """
    user = User.get_user(chat_id)
    price_range = {}
    if user.user_command == '/bestdeal':
        sortOrder = 'DISTANCE'
        price_range = {"price": {"max": user.price_max, "min": user.price_min}}
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

    for hotel in data_hotels['data']['propertySearch']['properties']:
        user.hotels_dict[hotel['id']] = {}
        hotel_dict = user.hotels_dict[hotel['id']]
        hotel_dict['name'] = hotel['name']
        hotel_dict['distance'] = hotel['destinationInfo']['distanceFromDestination']['value']
        hotel_dict['price_night'] = round(float(hotel['price']['lead']['amount']) * 62, 2)
        hotel_dict['total_price'] = (int(''.join(re.findall(r'\d+', (hotel['price']['displayMessages'][1]['lineItems'][0]['value'])))) * 62)

