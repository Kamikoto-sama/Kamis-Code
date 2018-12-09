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


class Useless:
    def __init__(self, db_file_name: str, auto_commit=False):
        db = sqlite3.connect(db_file_name)
        self.query = db.cursor().execute
        self.name = db_file_name
        self.commit = db.commit
        self.auto_commit = auto_commit

    def create(self, table_name: str, columns: dict, commit=False):
        """CREATE TABLE <table_name> (*<columns => col_name:col_type>)"""
        if type(table_name) != str or type(columns) != dict:
            raise ValueError('Wrong arguments type')

        columns = ['%s %s' % (i, columns[i]) for i in columns]
        self.query('CREATE TABLE %s' % table_name + ','.join(columns))
        if commit or self.auto_commit:
            self.commit()

    def get(self, what_columns: str, from_table: str, where='', order=''):
        """SELECT <what_columns> FROM <from_table>[ WHERE <where>][ ORDER BY <order>] -> list(data)"""
        what_columns = what_columns if len(what_columns) > 0 else '*'
        query = 'SELECT %s FROM %s' % (what_columns, from_table)
        query += ' WHERE %s' % where if where != '' else ''
        query += ' ORDER BY %s' % order if order != '' else ''
        return list(self.query(query))

    def delete(self, from_table: str, where='', commit=False):
        """DELETE FROM <from_table>[ WHERE <where>]"""
        query = 'DELETE FROM %s' % from_table
        query += ' WHERE %s' % where if where != '' else ''
        self.query(query)
        if commit or self.auto_commit:
            self.commit()

    def update(self, table_name: str, col_values: dict, where='', commit=False):
        """UPDATE <table_name> SET *<col_values => col_name:col_value>"""
        query = 'UPDATE %s SET ' % table_name
        values = ['%s=%s' % (i, col_values[i]) for i in col_values]
        query += ','.join(values)
        query += ' WHERE %s' % where if where != '' else ''
        self.query(query)
        if commit or self.auto_commit:
            self.commit()

    def add(self, table_name: str, values, commit=False):
        """INSERT INTO <table_name> VALUES (*<values>/*<values => col_name:col_value>)"""
        if type(values) is tuple:
            values = ','.join(values)
        elif type(values) is dict:
            values = ['%s=%s' % (i, values[i]) for i in values]
        else:
            raise ValueError('Values must be "tuple" or "dict"')

        self.query('INSERT INTO %s VALUES (%s)' % (table_name, ','.join(values)))
        if commit or self.auto_commit:
            self.commit()

    def table_exists(self, table_name: str):
        query = "SELECT count(*) FROM sqlite_master WHERE type='table'"
        query += " AND name='%s'" % table_name
        return self.query(query)

    def delete_column(self, table_name, *columns):
        ExSQLite.delete_column(self.name, table_name, *columns)

    def rename_column(self, table_name, column_name, new_name):
        ExSQLite.rename_column(self.name, table_name, column_name, new_name)