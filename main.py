from Bot_Commands.low_price import func_low_price
from Bot_Files.user_class import User
from Bot_Files.my_bot import my_bot
from Bot_Commands.help import user_help

from Bot_Files.callback_data import callback_data #Не удалять, принимает данные с кнопок


@my_bot.message_handler(commands=['start'])
def start(message) -> None:
    my_bot.send_message(message.from_user.id, "Привет, я бот для поиска отелей. \nВведи /help для списка команд")


@my_bot.message_handler(commands=['help'])
def call_help(message):
    user_help(message)


@my_bot.message_handler(commands=['lowprice'])
def lowprice(message):
    func_low_price(message)


@my_bot.message_handler(commands=['highprice'])
def highprice(message):
    """
    Обработка команды highprice
    """
    user = User.get_user(message.chat.id)
    user.user_command = 'highprice'
    my_bot.send_message(message.from_user.id, 'Введите название города: ')


@my_bot.message_handler(commands=['bestdeal'])
def bestdeal(message):
    """
    Обработка команды bestdeal
    """
    user = User.get_user(message.chat.id)
    user.user_command = 'bestdeal'
    my_bot.send_message(message.from_user.id, 'Введите название города: ')


@my_bot.message_handler(commands=['history'])
def history(message):
    """
    Обработка команды history
    """
    user = User.get_user(message.chat.id)
    user.user_command = 'history'
    my_bot.send_message(message.from_user.id, 'В разработке. /help')


@my_bot.message_handler(content_types=['text', 'image', 'audio', 'document', 'video'])
def get_message(message) -> None:
    """
    Обработка любых сообщений вне команд
    """
    my_bot.send_message(message.from_user.id, "Я тебя не понимаю. /help")


my_bot.polling(none_stop=True, interval=0)

