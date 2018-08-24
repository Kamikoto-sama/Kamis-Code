import sqlite3

def Delete_Column(DB_name,table_name, *columns):
	try:
		db = sqlite3.connect(DB_name)
		sql = db.cursor()
		#columns = iterCols if iterCols!=None and len(iterCols)!=0 else columns
		query = sql.execute("PRAGMA table_info(%s)" % table_name)
		query = list(query)
		
		if len(query) != 0:
				cols = {}
				for col in query:
					cols.setdefault(col[1],col[2])
				for col in columns:
					cols.pop(col)
				if len(cols) == 0:
					raise NameError

				query = ','.join(cols.keys())
				data = list(sql.execute("SELECT %s FROM " % query +table_name))
				sql.execute("DROP TABLE "+table_name)

				newCols = ''
				for col in cols.items():
					newCols += ' '.join(col)+','

				query = "CREATE TABLE {0} ({1})".format(table_name, newCols.strip(','))
				sql.execute(query)

				cols = ["?" for _ in range(len(cols))]
				query = "INSERT INTO "+table_name+" VALUES (%s)" % ','.join(cols)
				sql.executemany(query, data)
				db.commit()
				print("Colunms successfully deleted")
		else: print("NO SUCH TABLE")
	except sqlite3.OperationalError as e: print("Wrong arguments!")
	except NameError: print("COUNT OF COLUNMS IS LESS THEN 1 !")
	except (KeyError,TypeError): print("NO SUCH COLUNM!")
	except Exception as e: print("Something went wrong :(",e)

def Rename_Colunm(DB_name,table_name,colunm_name,new_name):
	try:
		db = sqlite3.connect(DB_name)
		sql = db.cursor()

		query = sql.execute("PRAGMA table_info(%s)" % table_name)
		query = list(query)
		
		if len(query) != 0 and colunm_name != new_name:
				cols = {}
				for col in query:
					cols.setdefault(col[1],col[2])

				query = ','.join(cols.keys())
				data = list(sql.execute("SELECT %s FROM " % query +table_name))
				
				sql.execute("ALTER TABLE "+table_name+" RENAME TO T_M_P")

				newCols = ''
				for col in cols.items():
					newCols += ' '.join(col)+','
				newCols = newCols.replace(colunm_name,new_name)
				query = "CREATE TABLE {0} ({1})".format(table_name, newCols.strip(','))
				sql.execute(query)

				cols = ["?" for _ in range(len(cols))]
				query = "INSERT INTO "+table_name+" VALUES (%s)" % ','.join(cols)
				sql.executemany(query, data)
				sql.execute("DROP TABLE T_M_P")
				db.commit()
				print("Something was done...")
		elif colunm_name == new_name:
			print("Wrong arguments!")
		else: print("NO SUCH TABLE")

	except sqlite3.OperationalError as e: 
		sql.execute("ALTER TABLE T_M_P RENAME TO "+table_name)
		print("Wrong arguments:",e)
	except Exception as e: 
		sql.execute("ALTER TABLE T_M_P RENAME TO "+table_name)
		print("Something went wrong :(",e)