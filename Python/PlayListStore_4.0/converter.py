from sqlite3 import connect as db_connect

file_name = "titles.txt"

def convert():
    db = db_connect("data.pls")
    sql = db.cursor().execute
    pl = ''
    icons = [0, 1, 3, 4, 5, 2]
    viewed = 0
    try:
        with open(file_name) as file:
            for index, t in enumerate(file.readlines()):
                t = t.rstrip().split('|')
                if pl != t[2]:
                    pl = t[2]
                    sql("INSERT INTO Playlists VALUES ('%s')" % pl)
                t[3] = icons[int(t[3])]
                if t[4] == "viewed":
                    viewed += 1
                elif t[4] == 'n' and t[3] == 2:
                    t[4] = 'pause'

                t[10] = 0 if t[10] == '' else int(t[10])
                t[9] = t[9].split('.')
                t[9].reverse()

                query = "INSERT INTO Titles VALUES " \
                        "('%s',%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s',%s,0)"
                sql(query % (t[0], int(t[1]), index, pl, t[3], t[4],
                             t[5], t[6], t[7], t[8], '.'.join(t[9]), t[10]))
            index = str(index + 1)
            sql("UPDATE Data SET value='%s' WHERE name='id'" % index)
            sql("UPDATE Data SET value='%s' WHERE name='viewed'" % str(viewed))
            sql("UPDATE Data SET value='%s' WHERE name='added'" % index)
            sql('INSERT INTO Data VALUES("cur_pl","0")')
            db.commit()
            print("Converted %s titles" % index)
    except FileNotFoundError:
        raise FileNotFoundError("Файл '%s' не найден" % file_name)
    except Exception as e:
        input(str(e))

if __name__ == '__main__':
    convert()