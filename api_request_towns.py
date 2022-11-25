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
        "X-RapidAPI-Key": "7a3d6d2995mshf9c37390f4ee1cep19c9c4jsnd3e2202a6ebc",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    end = json.loads(response.text)
    return end['sr']
