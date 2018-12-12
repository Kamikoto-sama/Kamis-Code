import sqlite3

db = sqlite3.connect('Data.pls')
SQL = db.cursor().execute

def sql(quary):
    answer = SQL(quary)
    db.commit()
    return list(answer)