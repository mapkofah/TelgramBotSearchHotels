from Bot_Commands.best_deal import func_best_deal
from Bot_Commands.low_price import func_low_price
from Bot_Files.user_class import User
from Bot_Files.my_bot import my_bot
from Bot_Commands.help import user_help
from Bot_Commands.high_price import func_high_price
from Bot_Files.callback_data import callback_data  # Не удалять, принимает данные с кнопок


@my_bot.message_handler(commands=['start'])
def start(message) -> None:
    my_bot.send_message(message.from_user.id, "Привет, я бот для поиска отелей. \nВведи /help для списка команд")


@my_bot.message_handler(commands=['help'])
def call_help(message) -> None:
    user_help(message)


@my_bot.message_handler(commands=['lowprice'])
def lowprice(message) -> None:
    func_low_price(message)


@my_bot.message_handler(commands=['highprice'])
def highprice(message) -> None:
    func_high_price(message)


@my_bot.message_handler(commands=['bestdeal'])
def bestdeal(message) -> None:
    func_best_deal(message)


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
