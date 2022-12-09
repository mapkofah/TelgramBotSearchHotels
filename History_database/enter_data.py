from Bot_Files.user_class import User
import sqlite3



def enter_data(chat_id):
    user = User.get_user(chat_id)
conn = sqlite3.connect('history.db')
cur = conn.cursor()
# Создание таблицы
# cur.execute("""CREATE TABLE IF NOT EXISTS history(
#    user_id INTEGER,
#    command TEXT,
#    date TEXT,
#    hotels TEXT);
# """)
# conn.commit()

# Добавление данных
id = 122
com = 'loww'
dat = '222'
hot = 'ppo'
# cur.execute("""INSERT INTO history(user_id, command, date, hotels)
#    VALUES(?, ?, ?, ?);""", (id, com, dat, hot))
# conn.commit()

# cur.execute("UPDATE history SET hotels = ? WHERE user_id = 123", hot)
#
# cur.execute("SELECT * FROM history;")
# all_results = cur.fetchall()
# print(all_results)
cur.execute("SELECT user_id FROM history;")
one_result = cur.fetchone()
print(one_result)