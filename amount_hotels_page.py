from my_bot import my_bot
from user_class import User
from need_photos import need_photo


def amount_hotels_page(message):
    """
    Спрашивает пользователя о количестве вывода отелей на странице
    """
    chat_id = message.chat.id

    msg = my_bot.send_message(chat_id, 'Введите желаемое количество результатов на странице\n'
                                       'Максимум 25')
    my_bot.register_next_step_handler(msg, check_amount)


def check_amount(message):
    chat_id = message.chat.id
    user = User.get_user(chat_id)
    try:
        amount = int(message.text)
        if amount > 25:
            raise ValueError
        user.hotels_amount = amount
        need_photo(message)
    except:
        my_bot.send_message(chat_id, 'Ошибка ввода, введите еще раз цифрами не больше 25')
        amount_hotels_page(message)
