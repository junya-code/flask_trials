import sqlite3

DATABASE = "database.db"


def init_db():
    with sqlite3.connect(DATABASE) as con:
        con.executescript(open("schema.sql", encoding="utf-8").read())
