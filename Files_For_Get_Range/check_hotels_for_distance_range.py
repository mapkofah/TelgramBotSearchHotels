import re
from typing import List

from Bot_Files.user_class import User


def check_hotels_distance(chat_id, hotels_list_api: List[dict]) -> List[dict] or None:
    user = User.get_user(chat_id)
    hotels_list = []
    for hotel in hotels_list_api:
        distance_miles = hotel['landmarks'][0]['distance']
        miles = re.search(r'\S*', distance_miles).group()
        distance_from_center = round(float(miles) * 1.7, 1)
        if distance_from_center < int(user.distance_min):
            continue
        hotels_list.append(hotel)

    if len(hotels_list) < len(hotels_list_api):
        user.flag_distance_min = True
        user.page_size_if_flag_min = int(user.page_size) - len(hotels_list)
    if len(hotels_list) > 0:
        user.flag_dist_min_range = True
        return hotels_list
    return None
