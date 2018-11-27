import sqlite3

class ExSQLite:
    @staticmethod
    def delete_column(db_name, table_name, *columns):
        try:
            db = sqlite3.connect(db_name)
            sql = db.cursor()
            query = sql.execute("PRAGMA table_info(%s)" % table_name)
            query = list(query)

            if len(query) != 0:
                cols = {}
                for col in query:
                    cols.setdefault(col[1], col[2])
                for col in columns:
                    cols.pop(col)
                if len(cols) == 0:
                    raise NameError

                query = ','.join(cols.keys())
                data = list(sql.execute("SELECT %s FROM " % query + table_name))
                sql.execute("DROP TABLE " + table_name)

                new_cols = ''
                for col in cols.items():
                    new_cols += ' '.join(col) + ','

                query = "CREATE TABLE {0} ({1})".format(table_name, new_cols.strip(','))
                sql.execute(query)

                cols = ["?" for _ in range(len(cols))]
                query = "INSERT INTO " + table_name + " VALUES (%s)" % ','.join(cols)
                sql.executemany(query, data)
                db.commit()
                print("Columns successfully deleted")
            else:
                print("NO SUCH TABLE")
        except sqlite3.OperationalError as e:
            print("Wrong arguments! ", e)
        except NameError:
            print("Count of columns IS LESS THEN 1 !")
        except (KeyError, TypeError):
            print("No such column!")
        except Exception as e:
            print("Something went wrong :(", e)

    @staticmethod
    def rename_column(db_name, table_name, column_name, new_name):
        try:
            db = sqlite3.connect(db_name)
            sql = db.cursor()

            query = sql.execute("PRAGMA table_info(%s)" % table_name)
            query = list(query)

            if len(query) != 0 and column_name != new_name:
                cols = {}
                for col in query:
                    cols.setdefault(col[1], col[2])

                query = ','.join(cols.keys())
                data = list(sql.execute("SELECT %s FROM " % query + table_name))

                sql.execute("ALTER TABLE " + table_name + " RENAME TO __TMP__")

                new_cols = ''
                for col in cols.items():
                    new_cols += ' '.join(col) + ','
                new_cols = new_cols.replace(column_name, new_name)
                query = "CREATE TABLE {0} ({1})".format(table_name, new_cols.strip(','))
                sql.execute(query)

                cols = ["?" for _ in range(len(cols))]
                query = "INSERT INTO " + table_name + " VALUES (%s)" % ','.join(cols)
                sql.executemany(query, data)
                sql.execute("DROP TABLE __TMP__")
                db.commit()
                print("Something has done...")
            elif column_name == new_name:
                print("Wrong arguments!")
            else:
                print("No such table!")

        except sqlite3.OperationalError as e:
            sql.execute("ALTER TABLE __TMP__ RENAME TO " + table_name)
            print("Wrong arguments:", e)
        except Exception as e:
            sql.execute("ALTER TABLE __TMP__ RENAME TO " + table_name)
            print("Something went wrong :(", e)

class SQLTerminal:
    pass