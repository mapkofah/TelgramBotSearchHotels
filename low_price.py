import json
import requests
from telebot import logger
from typing import Optional


# Команда /lowprice
# После ввода команды у пользователя запрашивается:
# 1. Город, где будет проводиться поиск.
# 2. Количество отелей, которые необходимо вывести в результате (не больше
# заранее определённого максимума).
# 3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
# a. При положительном ответе пользователь также вводит количество
# необходимых фотографий (не больше заранее определённого
# максимума)


def api_request(url: str, querystring: dict) -> Optional[dict]:
    """
    Функция отправки запроса к API
    :param url: url запроса
    :param querystring: параметр запроса в формате словаря
    """
    try:
        # response = requests.request("GET", url, headers=config.headers, params=, timeout=20)
        if response.status_code == 200:
            result = json.loads(response.text)
        else:
            result = None
    except requests.Timeout as time_end:
        logger.exception(time_end)
        result = None
    except requests.RequestException as er:
        logger.exception(er)
        result = None

    return result


def location_search(my_city: str) -> Optional[dict]:
    """
    Функция для поиска города по названию
    :param my_city: название города
    :return: данные в формате json либо None при отсутствии города в данных от API
    """
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": my_city, "locale": "ru_RU"}

    return api_request(url=url, querystring=querystring)

url = "https://hotels4.p.rapidapi.com/locations/v3/search"

querystring = {"q":"moscow","locale":"en_US","langid":"1033","siteid":"300000001"}

headers = {
	"X-RapidAPI-Key": "d9c90351d9msh10767cdef300ff9p16ad25jsn931121e2d5e6",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)