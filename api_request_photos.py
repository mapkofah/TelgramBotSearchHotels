from my_bot import my_bot
from user_class import User


def api_request_photo(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    my_bot.send_message(chat_id, 'Функция для загрузки фото отеля')