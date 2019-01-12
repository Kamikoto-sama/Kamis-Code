import sqlite3

db = sqlite3.connect('Data.pls')
SQL = db.cursor().execute

def sql(query):
    answer = SQL(query)
    db.commit()
    return list(answer)