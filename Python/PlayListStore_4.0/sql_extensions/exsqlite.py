def change_columns(db, table_name, change_type, *column_names, **column_changes):
    """db: sqlite3.connect\n
     change_type: enum(name, type, delete)\n
     if change_type="delete" column_names: *column_names
                        or column_changes: **(column_name: Any)
     if change_type="name" column_changes: **(column_name: new_name)\n
     if change_type="type" column_changes: **(column_name: new_type)"""
    try:
        sql = db.cursor().execute
        query = list(sql("PRAGMA table_info(%s)" % table_name))
        old_cols = dict()
        for col in query:
            null = "NOT NULL" if col[3] else ''
            default = '' if col[4] is None else "DEFAULT %s" % col[4]
            primary = "PRIMARY KEY" if col[5] else ''
            params = ' '.join((col[2], null, default, primary)).rstrip()
            old_cols[col[1]] = [col[1], params]

        if change_type == "name":
            for col in column_changes:
                old_cols[col][0] = column_changes[col]
        elif change_type == "delete":
            for col in (column_names if len(column_changes) == 0 else column_changes):
                old_cols.pop(col)
        elif change_type == "type":
            for col in column_changes:
                old_cols[col][1] = column_changes[col]
        else:
            raise ValueError

        new_columns = ','.join([' '.join(col) for col in old_cols.values()])
        new_data = (table_name, ','.join([c[0] for c in old_cols.values()]),
                    ','.join(old_cols.keys()), table_name + "_old_")

        sql("ALTER TABLE {0} RENAME TO {0}_old_".format(table_name))
        sql("CREATE TABLE %s (%s)" % (table_name, new_columns))
        sql("INSERT INTO %s (%s) SELECT %s FROM %s" % new_data)
        sql("DROP TABLE %s" % table_name + "_old_")
        db.commit()
        print("Done")
        if len(column_names) == len(column_changes) == 0:
            print("But nothing has changed :|")
    except ValueError:
        raise ValueError("Unknown change type")
    except KeyError:
        raise ValueError("No such column")
    except Exception as e:
        raise Exception("You fucked because %s" % str(e))
