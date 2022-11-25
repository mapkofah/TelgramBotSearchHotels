import requests
import json


def data_town(name: str, gaiaId: str) -> str:
    """
    Функция для запроса destinationId города с API Hotels.com
    :param name: Название города
    :param gaiaId: gaiaId города для
    """
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": name, "locale": "ru_RU", "currency": "USD"}

    headers = {
        "X-RapidAPI-Key": "7a3d6d2995mshf9c37390f4ee1cep19c9c4jsnd3e2202a6ebc",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    end = json.loads(response.text)
    list_town = end['suggestions'][0]['entities']
    for item in list_town:
        if item['geoId'] == gaiaId:
            destinationId = item['destinationId']  # Нашли верный destinationId
            return destinationId
