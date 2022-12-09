import time

from Bot_Files.my_bot import my_bot
from Bot_Files.user_class import User


def func_history(message) -> None:
    """
    Обработка команды history
    """
    chat_id = message.chat.id
    user = User.get_user(message.chat.id)
    user.user_command = 'history'
    tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))  # Конвертация даты в читабельный вид
    my_bot.send_message(chat_id, f"{tconv(message.date)} {message.date}")
