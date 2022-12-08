from Bot_Commands.help import user_help
from Bot_Files.my_bot import my_bot
from Bot_Files.user_class import User
from Files_For_Get_Hotels.amount_hotels_page import amount_hotels_page


def distance_range(message) -> None:
    chat_id = message.chat.id
    msg = my_bot.send_message(chat_id, 'Введите максимальное расстояние (км)')
    my_bot.register_next_step_handler(msg, check_distance)


def check_distance(message) -> None:
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    try:
        int(message.text)
        if message.text == '/help' or message.text == '/start':
            raise FileNotFoundError
    except FileNotFoundError:
        user_help(message)
    except ValueError:
        msg = my_bot.send_message(chat_id, 'Неверный ввод, вводите расстояние цифрами')
        distance_range(msg)
    else:
        user.distance_range = int(message.text)
        amount_hotels_page(message)
