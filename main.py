import requests
from my_bot import my_bot


@my_bot.message_handler(commands=['start', 'help', 'lowprice', 'highprice', 'bestdeal', 'history'])
def get_command(message) -> None:
    if message.text == '/start':
        my_bot.send_message(message.from_user.id, "Привет, я бот для поиска отелей. \nВведи /help для списка команд")
    elif message.text == '/help':
        my_bot.send_message(message.from_user.id, '/lowprice: Топ самых дешёвых отелей в городе.\n'
                                                  '/highprice: Топ самых дорогих отелей в городе.\n'
                                                  '/bestdeal: Топ отелей, наиболее дешёвых и ближе всего к центру.\n'
                                                  '/history Узнать историю поиска отелей')
    elif message.text == '/lowprice':
        my_bot.send_message(message.from_user.id, 'В разработке. /help')
    elif message.text == '/highprice':
        my_bot.send_message(message.from_user.id, 'В разработке. /help')
    elif message.text == '/bestdeal':
        my_bot.send_message(message.from_user.id, 'В разработке. /help')
    elif message.text == '/history':
        my_bot.send_message(message.from_user.id, 'В разработке. /help')


@my_bot.message_handler(content_types=['text'])
def get_message(message) -> None:
    if message.text:
        my_bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


def get_town_in_api(message):
    pass

my_bot.polling(none_stop=True, interval=0)
