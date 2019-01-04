import sqlite3
import os

db_name = "Data.pls"

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
            icon varchar(15),
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

if __name__ == "__main__":
    if os.path.exists(db_name):
        os.remove(db_name)
    create_db()