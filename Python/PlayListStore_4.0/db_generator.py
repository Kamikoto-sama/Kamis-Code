import sqlite3
import os
from random import randint

db_name = "Data.pls"
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def create_db():
    db = sqlite3.connect(db_name)
    sql = db.cursor().execute
    sql('CREATE TABLE Playlists (name varchar(30))')
    sql("CREATE TABLE Data (name varchar(10), value varchar(40))")
    sql("""
            CREATE TABLE Titles (
            title_name varchar(60) NOT NULL,
            count int(4),
            id integer PRIMARY KEY AUTOINCREMENT,
            playlist varchar(100),
            icon int(10),
            color varchar(15),
            genre varchar(60),
            link text,
            desc text,
            con_date varchar(10),
            date varchar(10)
            )""")

    sql('INSERT INTO Data VALUES("id","0")')
    sql('INSERT INTO Data VALUES("viewed","0")')
    sql('INSERT INTO Data VALUES("added","0")')
    sql('INSERT INTO Data VALUES("cur_pl","-1")')
    db.commit()


def add_titles(sql, pl_name, t_count, id_, **flags):
    if not flags:
        flags['count'] = 0
    for i in range(t_count):
        name = alpha[i] if i < 52 else str(i)
        count = flags['count'] if not flags and flags['count'] else randint(1, 200)
        genre = alpha[:randint(1, 20)]
        desc = alpha[:randint(1, 52)]
        title = (name, count, id_, pl_name, 3, 'n', genre, '', desc, '04.01.2019')
        query = "INSERT INTO Titles VALUES "
        sql(query + "('%s',%s,%s,'%s','%s','%s','%s','%s','%s','', '%s')" % title)
        id_ += 1

    sql("UPDATE Data SET value='%s' WHERE name='id'" % id_)
    sql("UPDATE Data SET value='%s' WHERE name='added'" % t_count)
    return id_


def add_playlist(sql, name):
    sql("INSERT INTO Playlists VALUES ('%s')" % name)
    sql("UPDATE Data SET value='0' WHERE name='cur_pl'")

def generate_data(sql, db, pl_count, title_count):
    id_ = 0

    for i in range(pl_count):
        pl_name = "PL%s" % i
        add_playlist(sql, pl_name)
        id_ = add_titles(sql, pl_name, title_count, id_)

    db.commit()


def init():
    print("Exit - Enter\nGen data - 0\nXTitle - 1")
    req = input()
    os.remove(db_name)
    create_db()
    db = sqlite3.connect(db_name)
    sql = db.cursor().execute
    if req == '':
        return
    if req == '0':
        req = input("pl_count titles_count: ").split()
        generate_data(sql, db, int(req[0]), int(req[1]))
    if req == '1':
        req = input("title_count count: ").split()
        add_playlist(sql, "PL1")
        add_titles(sql, "PL1", int(req[0]), 0, count=int(req[1]))
        db.commit()

    print("Done...\n")

if __name__ == "__main__":
    init()
