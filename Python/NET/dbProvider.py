import os
import sqlite3

allowedDbFormats = (".db",)

class DataBaseProvider:
	def __init__(self):
		self.dataBaseName = None
	
	def getDbConnection(self):
		if self.dataBaseName is None:
			self.dataBaseName = self.__getDbName()
			
		connection = sqlite3.connect(self.dataBaseName)
		return connection
	
	@staticmethod
	def __getDbName():
		files = os.listdir(".")
		for f in files:
			if f.endswith(allowedDbFormats):
				return f