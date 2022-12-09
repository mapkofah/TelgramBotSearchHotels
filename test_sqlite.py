import sqlite3
conn = sqlite3.connect(r'History_database\history.db')
cur = conn.cursor()
# Создание таблицы
cur.execute("""CREATE TABLE IF NOT EXISTS history(
   command TEXT,
   date INTEGER,
   hotels LIST);
""")
conn.commit()
# Добавление данных
# cur.execute("""INSERT INTO history(command, date, hotels)
#    VALUES('lowprice', '2022222', 'lossantos');""")
# conn.commit()
command = 'low'
date = 2022
hotels = ('1', '2')
data = (command, date, hotels)
cur.execute("INSERT INTO history VALUES(?, ?, ?);", data)
conn.commit()

cur.execute("SELECT * FROM history;")
all_results = cur.fetchall()
print(all_results)

# cur.execute("""SELECT *, users.fname, users.lname FROM orders
#     LEFT JOIN users ON users.userid=orders.userid;""")
# print(cur.fetchall())

#Нужно создать базу данных отелей, бд юзера, бд дат
#потом объединяЕм
#
#
#
#
#
#
#
#