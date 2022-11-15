import json
import re
import requests
from googletrans import Translator


name_town = 'нью йорк'

# Ищем город и любые совпадения по последнему способу, для нахождения gaiaId
url = "https://hotels4.p.rapidapi.com/locations/v3/search"

querystring = {"q": name_town, "locale": "ru_RU", "langid": "1034", "siteid": "300000001"}

headers = {
    "X-RapidAPI-Key": "d9c90351d9msh10767cdef300ff9p16ad25jsn931121e2d5e6",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}
response = requests.request("GET", url, headers=headers, params=querystring)
end = json.loads(response.text)
list_town = end['sr']
for item in list_town:
    if item['type'] == 'CITY':
        word = item['regionNames']["fullName"] # Полное название города
        if word.startswith('New York'):
            gaia_id = item['gaiaId'] # gaiaId
            break

# Ищем предпоследним способом destinationId по gaiaId
url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query": name_town, "locale": "en_US", "currency": "USD"}

headers = {
    "X-RapidAPI-Key": "d9c90351d9msh10767cdef300ff9p16ad25jsn931121e2d5e6",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
end = json.loads(response.text)
list_town = end['suggestions'][0]['entities']
for item in list_town:
    if item['geoId'] == gaia_id:
        destinationId = item['destinationId']  # Нашли верный destinationId

# Выводим список отелей 10 штук на странице


url = "https://hotels4.p.rapidapi.com/properties/list"

querystring = {"destinationId": destinationId, "pageNumber": "1", "pageSize": "10", "checkIn": "2022-11-12",
               "checkOut": "2022-11-13", "adults1": "1", "sortOrder": "PRICE", "locale": "en_US", "currency": "USD"}

headers = {
    "X-RapidAPI-Key": "d9c90351d9msh10767cdef300ff9p16ad25jsn931121e2d5e6",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
end = json.loads(response.text)

with open('test_file_for_town.json', 'w') as file:
    json.dump(end['data']['body']['searchResults']['results'], file, indent=4)
# Если в ключе deals, нет значений, значит предложение отсутствует
# На сайте сортировка идет не по порядку
