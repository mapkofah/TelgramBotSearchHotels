from high_price import func_high_price
from low_price import func_low_price
from user_class import User
from my_bot import my_bot
from help import user_help
#Не удалять, принимает данные с кнопок
from callback_data import callback_data


@my_bot.message_handler(commands=['start'])
def start(message) -> None:
    my_bot.send_message(message.from_user.id, "Привет, я бот для поиска отелей. \nВведи /help для списка команд")


@my_bot.message_handler(commands=['help'])
def call_help(message) -> None:
    user_help(message)


@my_bot.message_handler(commands=['lowprice'])
def lowprice(message) -> None:
    """
    Обработка команды lowprice
    """
    func_low_price(message)


@my_bot.message_handler(commands=['highprice'])
def highprice(message) -> None:
    """
    Обработка команды highprice
    """
    func_high_price(message)


@my_bot.message_handler(commands=['bestdeal'])
def bestdeal(message) -> None:
    """
    Обработка команды bestdeal
    """
    user = User.get_user(message.chat.id)
    user.user_command = 'bestdeal'
    my_bot.send_message(message.from_user.id, 'Введите название города: ')


@my_bot.message_handler(commands=['history'])
def history(message) -> None:
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

