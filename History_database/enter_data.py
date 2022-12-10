from Bot_Files.user_class import User
import sqlite3


def enter_first_data(chat_id) -> None:
    """
    Функция ввода данных в базу данных history, для команды /history
    """
    user = User.get_user(chat_id)

    conn = sqlite3.connect(r'History_database\history.db')  # Подключаемся к sql
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS history( 
       id INTEGER,
       chat_id INTEGER,
       command TEXT,
       date TEXT,
       hotels TEXT);
    """)  # Создаем таблицу
    conn.commit()

    cur.execute("SELECT id FROM history WHERE chat_id='%s'" % chat_id)
    last_id = cur.fetchall()[-1:]
    # Создание первой записи в таблице. Добавление id, command, date
    if not last_id:
        cur.execute("""INSERT INTO history (id, chat_id, command, date) VALUES(?, ?, ?, ?)""",
                    (user.data_id, chat_id, user.user_command, user.date_message))
        conn.commit()
    else:
        user.data_id = last_id[0][0] + 1
        cur.execute("""INSERT INTO history (id, chat_id, command, date) VALUES(?, ?, ?, ?)""",
                    (user.data_id, chat_id, user.user_command, user.date_message))
        conn.commit()
    conn.close()  # Закрытие базы


def enter_hotels_names(chat_id) -> None:
    user = User.get_user(chat_id)

    conn = sqlite3.connect(r'History_database\history.db')  # Подключаемся к sql
    cur = conn.cursor()
    cur.execute("SELECT hotels FROM history WHERE chat_id= ? AND id= ?", (chat_id, user.data_id))
    old_hotels = cur.fetchone()[0]
    hotels = ', '.join(user.hotels_names)
    if not old_hotels:
        cur.execute("UPDATE history SET hotels = ? WHERE chat_id= ? AND id = ?", (hotels, chat_id, user.data_id))
        conn.commit()
    else:
        hotels = hotels + ', ' + old_hotels
        cur.execute("UPDATE history SET hotels = ? WHERE chat_id= ? AND id = ?", (hotels, chat_id, user.data_id))
        conn.commit()
    conn.close()

