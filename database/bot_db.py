import sqlite3

import sqlite3
import random
from config import bot

def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")
    db.execute("CREATE TABLE IF NOT EXISTS dishes "
               "(id INTEGER PRIMARY KEY,"
               "photo TEXT, name TEXT PRIMARY KEY, description TEXT,"
               "price INTEGER)")
    db.commit()

async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO deshes VALUES (?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()

async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM dishes").fetchall()
    random_user = random.randint(0, len(result) - 1)
    await bot.send_photo(message.from_user.id,
                         result[random_user][2],
                         caption = f"photo: {result[random_user][3]}\n"
                                   f"name dish: {result[random_user][4]}\n"
                                   f"description: {result[random_user][5]}\n"
                                   f"price: {result[random_user][6]}\n\n"
                                   f"{result[random_user][1]}\n")

async def sql_command_all():
    return cursor.execute("SELECT * FROM dishes").fetchall()

async def sql_command_delete(id):
    cursor.execute("DELETE FROM dishes WHERE id == ?", (id,))
    db.commit()