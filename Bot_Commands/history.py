from History_database.send_data import send_history


def func_history(message) -> None:
    """
    Обработка команды history
    """
    chat_id = message.chat.id
    send_history(chat_id)
