from functools import reduce
from sqlite3 import Connection

class DataBaseController:
	def __init__(self, db: Connection):
		self.db = db
		
	def get(self, tableName, params=None, sorting=None):
		params = f"WHERE {params}" if params is not None else ""
		sorting = f"ORDER BY {sorting}" if sorting is not None else ""
		query = f"SELECT * FROM {tableName} {params} {sorting}"
		result = self.db.execute(query)
		return result
		
	def add(self, tableName, values):
		query = f"INSERT INTO {tableName} VALUES {values}".replace("'null'", "null")
		self.db.execute(query)
		self.db.commit()
		
	def update(self, tableName, values: dict, params=None):
		params = f"WHERE {params}" if params is not None else ""
		query = f"UPDATE {tableName} SET {values} {params}".replace("'null'", "null")
		self.db.execute(query)
		self.db.commit()
		
	def delete(self, tableName, params=None):
		params = f"WHERE {params}" if params is not None else ""
		query = f"DELETE FROM {tableName} {params}"
		self.db.execute(query)
		self.db.commit()
		
	def toDictObj(self, tableName, rows):
		query = f"select name from pragma_table_info({tableName!r})"
		columnNames = reduce(lambda x,s: x+s, self.db.execute(query))
		for row in rows:
			yield {col:val for col, val in zip(columnNames, row)}