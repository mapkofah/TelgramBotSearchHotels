import json
from typing import List
import requests
from Bot_Files.user_class import User


def api_request_hotel(message) -> List[dict]:
    """
    Функция получения данных с API Hotels.com об отелях
    """
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    if user.user_command == '/lowprice':
        sortOrder = 'PRICE'
    elif user.user_command == '/highprice':
        sortOrder = 'PRICE_HIGHEST_FIRST'
    else:
        sortOrder = 'DISTANCE_FROM_LANDMARK'
        # Самые дешевые и находятся ближе всего к центру
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": user.city_id, "pageNumber": user.page_num, "pageSize": user.page_size,
                   "checkIn": user.check_in,
                   "checkOut": user.check_out, "adults1": "2", "sortOrder": sortOrder, "locale": "en_US",
                   "currency": "RUB"}

    headers = {
        'X-RapidAPI-Key': '9394540643mshe2529c27c22b9a8p114570jsna1c6d35226f3',
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    end = json.loads(response.text)

    return end['data']['body']["searchResults"]['results']
