import json
from typing import Tuple, List
import requests


def api_request_towns(name: str) -> List[dict]:
    """
    Функция получения данных с API Hotels.com о предложенных города
    :param name: Название города
    :return: Список городов подходящих под введенное название
    """
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": name, "locale": "ru_RU", "langid": "1034", "siteid": "300000001"}

    headers = {
        "X-RapidAPI-Key": "d9c90351d9msh10767cdef300ff9p16ad25jsn931121e2d5e6",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    end = json.loads(response.text)
    return end['sr']
