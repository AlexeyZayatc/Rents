import sqlite3

with open("db_commands.txt","r",encoding="utf-8") as f:
    commands = f.read()
    conn = sqlite3.connect("rentdb.sqlite")
    cursor = conn.cursor()
    cursor.executescript(commands)
    cursor.close()
    conn.close()

