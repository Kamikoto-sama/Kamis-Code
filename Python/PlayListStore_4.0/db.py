import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui

db = sqlite3.connect('Data.pls')
SQL = db.cursor()

def sql(quary):
    answer = SQL.execute(quary)
    db.commit()
    return answer