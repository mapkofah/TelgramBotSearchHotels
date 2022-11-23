from my_bot import my_bot
from user_class import User


def api_request_hotel(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    my_bot.send_message(chat_id, 'Здесь будет функция для загрузки отелей с сайта')
#Загружаем список отелей с сайта
#Проверяем доступность вариантов
#Сохраняем список
#Выводим пользователю в нужном количестве на кнопках(с фото или без) с ценой
#Делаем несколько страниц с перелистыванием
