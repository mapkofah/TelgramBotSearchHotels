from Bot_Commands.help import user_help
from Bot_Files.my_bot import my_bot
from Bot_Files.user_class import User
from Files_For_Get_Range.get_distance_range import distance_range


def price_range(message) -> None:
    chat_id = message.chat.id
    msg = my_bot.send_message(chat_id, 'Введите максимальную цену:')
    my_bot.register_next_step_handler(msg, check_price)


def check_price(message) -> None:
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    try:
        int(message.text)
        if message.text == '/help' or message.text == '/start':
            raise FileNotFoundError
    except FileNotFoundError:
        user_help(message)
    except ValueError:
        msg = my_bot.send_message(chat_id, 'Неверный ввод, вводите цену цифрами')
        price_range(message)
    else:
        user.price_range = int(message.text) / 62
        distance_range(message)
