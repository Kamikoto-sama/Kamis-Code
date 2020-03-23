from functools import reduce
from sqlite3 import Connection

class DataBaseController:
	def __init__(self, db: Connection):
		self._dbConnection = db
		
	def _read(self, tableName, params=None, sorting=None):
		params = f"WHERE {params}" if params is not None else ""
		sorting = f"ORDER BY {sorting}" if sorting is not None else ""
		query = f"SELECT * FROM {tableName} {params} {sorting}"
		result = self._dbConnection.execute(query)
		return self.__rowsToDictionary(tableName, result)
		
	def __rowsToDictionary(self, tableName, rows):
		query = f"select name from pragma_table_info({tableName!r})"
		columnNames = reduce(lambda x,s: x+s, self._dbConnection.execute(query))
		return [{col:val for col, val in zip(columnNames, row)} for row in rows]
		
	def _create(self, tableName, values, colNames=""):
		query = f"INSERT INTO {tableName} {colNames} VALUES {values}".replace("None", "null")
		self._dbConnection.execute(query)
		self._dbConnection.commit()
		
	def _update(self, tableName, updatedValues: dict, params=None):
		params = f"WHERE {params}" if params is not None else ""
		values = ",".join([f"{key}={value!r}" for key, value in updatedValues.items()])
		query = f"UPDATE {tableName} SET {values} {params}".replace("None", "null")
		self._dbConnection.execute(query)
		self._dbConnection.commit()
		
	def _delete(self, tableName, params=None):
		params = f"WHERE {params}" if params is not None else ""
		query = f"DELETE FROM {tableName} {params}"
		self._dbConnection.execute(query)
		self._dbConnection.commit()