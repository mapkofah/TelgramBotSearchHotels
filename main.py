import json
from typing import Callable, Optional

import requests
from googletrans import Translator
from my_bot import my_bot


@my_bot.message_handler(commands=['start'])
def start(message) -> None:
    my_bot.send_message(message.from_user.id, "Привет, я бот для поиска отелей. \nВведи /help для списка команд")


@my_bot.message_handler(commands=['help'])
def call_help(message):
    my_bot.send_message(message.from_user.id, '/lowprice: Топ самых дешёвых отелей в городе.\n'
                                              '/highprice: Топ самых дорогих отелей в городе.\n'
                                              '/bestdeal: Топ отелей, наиболее дешёвых и ближе всего к центру.\n'
                                              '/history Узнать историю поиска отелей')


@my_bot.message_handler(commands=['lowprice'])
def lowprice(message):
    get_town(message)

@my_bot.message_handler(commands=['highprice'])
def highprice(message):
    my_bot.send_message(message.from_user.id, 'Введите название города: ')


@my_bot.message_handler(commands=['bestdeal'])
def bestdeal(message):
    my_bot.send_message(message.from_user.id, 'Введите название города: ')


@my_bot.message_handler(commands=['history'])
def history(message):
    my_bot.send_message(message.from_user.id, 'В разработке. /help')


@my_bot.message_handler(content_types=['text', 'image', 'audio', 'document'])
def get_message(message) -> None:
    my_bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


def get_town(message):
    chat_id = message.chat.id
    msg = my_bot.send_message(chat_id, 'Введите название города: ')
    my_bot.register_next_step_handler(msg, get_towns_in_api)


def get_towns_in_api(message):
    chat_id = message.from_user.id
    translator = Translator()
    name_town = translator.translate(message.text).text
    towns_list = api_request_towns(name_town)
    my_bot.send_message(chat_id, 'Выберите ваш вариант')
    for item in towns_list:
        if item['type'] == 'CITY':
            town_name = item['regionNames']["fullName"]
            my_bot.send_message(chat_id, f'{town_name}')


def api_request_towns(name):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": name, "locale": "en_US", "langid": "1034", "siteid": "300000001"}

    headers = {
        "X-RapidAPI-Key": "d9c90351d9msh10767cdef300ff9p16ad25jsn931121e2d5e6",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    end = json.loads(response.text)
    return end['sr']


def get_date_in(message):
    return message.text

my_bot.polling(none_stop=True, interval=0)
