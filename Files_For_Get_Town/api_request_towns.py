import json
from typing import List

import requests


def api_request_towns(name: str) -> List[dict]:
    """
    Функция получения данных с API Hotels.com о предложенных городах
    :param name: Название города
    :return: Список городов подходящих под введенное название
    """
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": name, "locale": "ru_RU", "langid": "1034", "siteid": "300000001"}

    headers = {
        'X-RapidAPI-Key': '1796f32a87msh6ff0e54218bd17cp132c92jsnec17a594ba8d',
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    end = json.loads(response.text)
    return end['sr']
