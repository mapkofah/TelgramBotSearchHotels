import sqlite3

from Bot_Files.my_bot import my_bot


def send_history(chat_id):
    conn = sqlite3.connect(r'History_database\history.db')  # Подключаемся к sql
    cur = conn.cursor()
    cur.execute("SELECT command, date, hotels FROM history WHERE chat_id = '%s'" % chat_id)  # Вывод всей таблицы
    all_results = cur.fetchall()
    for result in all_results:
        my_bot.send_message(chat_id, f'Команда:{result[0]}\n'
                                     f'Дата: {result[1]}\n'
                                     f'Отели: {result[2]}')
    conn.close()

