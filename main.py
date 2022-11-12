import requests
from my_bot import my_bot


@my_bot.message_handler(content_types=['text'])
def get_messages(message) -> None:
    if message.text == '/start':
        my_bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text.lower() == "привет":
        my_bot.send_message(message.from_user.id, "Привет-Привет!")
    elif message.text == '/hello-world':
        my_bot.send_message(message.from_user.id, 'Hello World. Это мой первый бот Телеграм')
    elif message.text == '/help':
        my_bot.send_message(message.from_user.id, 'Напиши привет либо /hello_world')
    else:
        my_bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


my_bot.polling(none_stop=True, interval=0)
