import sqlite3

db = sqlite3.connect('data.pls')
SQL = db.cursor().execute

def sql(query):
    answer = SQL(query)
    db.commit()
    return list(answer)