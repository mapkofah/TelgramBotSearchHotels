import json
import requests


def api_request_photo(hotel_id):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    headers = {
        'X-RapidAPI-Key': '9394540643mshe2529c27c22b9a8p114570jsna1c6d35226f3',
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    end = json.loads(response.text)
    with open('my_test_photo.json', 'w') as file:
        json.dump(end['hotelImages'], file)
    return end['hotelImages']
