from my_bot import my_bot
from user_class import User


def output_hotels(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    if user.need_to_get_photo:
        index = 0
        for key, value in user.dict_photos.items():
            my_bot.send_message(chat_id, user.hotels_list[index])
            # Переделать hotels_list and dict_photos в один hotels_list
            index += 1
            my_bot.send_media_group(chat_id, value)
    else:
        for hotel in user.hotels_list:
            my_bot.send_message(chat_id, hotel)
