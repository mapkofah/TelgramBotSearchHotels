from telebot import types

from Files_For_Get_Photos.api_request_photos import api_request_photo
from Bot_Files.user_class import User


def get_photo(chat_id):
    user = User.get_user(chat_id)
    for hotel_id, photo_list in user.dict_photos.items():
        list_photos = api_request_photo(hotel_id)
        for index in range(user.amount_photo):
            url_photo = list_photos[index]['baseUrl'][:-10] + 'z.jpg'
            photo_list.append(types.InputMediaPhoto(url_photo))
