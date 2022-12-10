from Bot_Files.my_bot import my_bot
from Bot_Files.user_class import User


def user_help(message) -> None:
    chat_id = message.chat.id
    User.del_user(chat_id)
    User.get_user(chat_id)
    my_bot.send_message(message.from_user.id, '/lowprice: Топ самых дешёвых отелей в городе.\n'
                                              '/bestdeal: Топ отелей, наиболее дешёвых и ближе всего к центру.\n'
                                              '/history Узнать историю поиска отелей')