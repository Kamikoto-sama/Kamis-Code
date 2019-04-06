import os
import sys
import sqlite3
from main import Icons
from random import randint

db_name = "data.pls"
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
config_file = "db_generator.config"


def create_db(sql):
    sql('CREATE TABLE Playlists (name varchar(30))')
    sql("CREATE TABLE Data (name varchar(20), value varchar(40))")
    sql("""
            CREATE TABLE Titles (
            title_name varchar(80),
            count int(4),
            id integer PRIMARY KEY,
            playlist varchar(100),
            icon int(10),
            color varchar(15),
            genre varchar(60),
            link text,
            desc text,
            con_date varchar(10),
            date varchar(10),
            episode int(4),
            favorite int(4)
            )""")

    sql('INSERT INTO Data VALUES("id","0")')
    sql('INSERT INTO Data VALUES("viewed","0")')
    sql('INSERT INTO Data VALUES("added","0")')
    sql('INSERT INTO Data VALUES("cur_pl","-1")')
    sql('INSERT INTO Data VALUES("auto_update","0")')

def add_titles(sql, pl_name, t_count, id_, fix_count=0, perms=False, **kwargs):
    if perms:
        perms = list(Icons.values())
        t_count = len(perms)
    for i in range(t_count):
        name = alpha[i] if i < 52 else str(i)
        count = fix_count if fix_count else randint(1, 200)
        icon = perms[i] if perms else Icons['n']
        color = 'viewed' if perms in ['con', 'viewed'] else 'n'
        genre = alpha[:randint(1, 20)]
        desc = alpha[:randint(1, 52)]
        fav = -1
        if kwargs.get("fav", False):
            fav = i + 1

        title = (name, count, id_, pl_name, icon, color, genre,
                 '', desc, '04.01.2019', fav)
        query = "INSERT INTO Titles VALUES "
        sql(query + "('%s',%s,%s,'%s','%s','%s','%s','%s','%s','', '%s', 0, %s)" % title)
        id_ += 1

    sql("UPDATE Data SET value='%s' WHERE name='id'" % id_)
    sql("UPDATE Data SET value='%s' WHERE name='added'" % t_count)
    return id_


def add_playlist(sql, name):
    sql("INSERT INTO Playlists VALUES ('%s')" % name)
    sql("UPDATE Data SET value='0' WHERE name='cur_pl'")

def generate_data(sql, pl_count, title_count):
    id_ = 0

    for i in range(pl_count):
        pl_name = "PL%s" % i
        add_playlist(sql, pl_name)
        id_ = add_titles(sql, pl_name, title_count, id_)


def init():
    print("Exit: Enter\n"
          "Load conf: -\n"
          "Save configuration: +\n"
          "Gen data: 0\n"
          "Fixed titles: 1\n"
          "Mixed title: 2\n"
          "Start with params: 3")

    req = input() if len(sys.argv) <= 1 else ''
    if os.path.exists(db_name):
        os.remove(db_name)
    db = sqlite3.connect(db_name)
    sql = db.cursor().execute
    create_db(sql)

    set_conf = 0
    configurations = None
    if req == '+':
        set_conf = 1
        configurations = list()
        req = input()
        configurations.append(req)
    elif req == '-':
        set_conf = -1
        with open(config_file, 'r') as file:
            configurations = file.readline().split('|')
            req = configurations[0]

    if req == '':
        db.commit()
        return
    if req == '0':
        if set_conf >= 0:
            req = input("pl_count titles_count: ")
        if set_conf == 1:
            configurations.append(req)
            with open(config_file, 'w') as file:
                file.write('|'.join(configurations))
        elif set_conf == -1:
            req = configurations[1]
        req = req.split()

        generate_data(sql, int(req[0]), int(req[1]))
        db.commit()
        return

    add_playlist(sql, "PL1")
    if req == '1':
        if set_conf >= 0:
            req = input("title_count count: ")
        if set_conf == 1:
            configurations.append(req)
        elif set_conf == -1:
            req = configurations[1]
        req = req.split()
        add_titles(sql, "PL1", int(req[0]), 0, fix_count=int(req[1]))
    if req == '2':
        add_titles(sql, "PL1", 0, 0, fix_count=12, perms=True)
    if req == '3':
        if set_conf >= 0:
            req = input("option t_count: ")
        if set_conf == 1:
            configurations.append(req)
        elif set_conf == -1:
            req = configurations[1]
        req = req.split()
        add_titles(sql, "PL1", int(req[1]), 0, **{req[0]: True})

    if set_conf == 1:
        with open(config_file, 'w') as file:
            file.write('|'.join(configurations))
    db.commit()

if __name__ == "__main__":
    init()
    print("Done...\n")