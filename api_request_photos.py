import json
import requests


def api_request_photo(hotel_id):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    headers = {
        "X-RapidAPI-Key": "7a3d6d2995mshf9c37390f4ee1cep19c9c4jsnd3e2202a6ebc",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    end = json.loads(response.text)

    return end['hotelImages']

