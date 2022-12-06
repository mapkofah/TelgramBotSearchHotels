from Bot_Commands.help import user_help
from Bot_Files.my_bot import my_bot
from Bot_Files.user_class import User
from Files_For_Get_Photos.need_photos import need_photo


def amount_hotels_page(message):
    """
    Спрашивает пользователя о количестве вывода отелей на странице
    """
    chat_id = message.chat.id

    msg = my_bot.send_message(chat_id, 'Введите желаемое количество результатов на странице (макс 10)')
    my_bot.register_next_step_handler(msg, check_amount)


def check_amount(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    try:
        amount = int(message.text)
        if amount < 0 or amount > 10:
            raise OverflowError
        if message.text == '/help' or message.text == '/start':
            raise FileNotFoundError
    except ValueError:
        my_bot.send_message(chat_id, 'Ошибка ввода, введите еще раз, но только цифрами')
        my_bot.send_message(chat_id, 'Для возврата к началу /help')
        check_amount(message)
    except FileNotFoundError:
        user_help(message)
    except OverflowError:
        my_bot.send_message(chat_id, 'Ошибка ввода, введите число не меньше 1 и не больше 25')
        my_bot.send_message(chat_id, 'Для возврата к началу /help')
        check_amount(message)
    else:
        user.page_size = amount
        need_photo(message)
