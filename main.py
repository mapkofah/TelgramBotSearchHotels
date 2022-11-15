from user_class import User
from my_bot import my_bot
from get_town import get_town


@my_bot.message_handler(commands=['start'])
def start(message) -> None:
    user = User.get_user(message.chat.id)
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
    user = User.get_user(message.chat.id)
    user.user_command = 'highprice'
    my_bot.send_message(message.from_user.id, 'Введите название города: ')


@my_bot.message_handler(commands=['bestdeal'])
def bestdeal(message):
    user = User.get_user(message.chat.id)
    user.user_command = 'bestdeal'
    my_bot.send_message(message.from_user.id, 'Введите название города: ')


@my_bot.message_handler(commands=['history'])
def history(message):
    user = User.get_user(message.chat.id)
    user.user_command = 'history'
    my_bot.send_message(message.from_user.id, 'В разработке. /help')


@my_bot.message_handler(content_types=['text', 'image', 'audio', 'document', 'video'])
def get_message(message) -> None:
    my_bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")

my_bot.polling(none_stop=True, interval=0)

