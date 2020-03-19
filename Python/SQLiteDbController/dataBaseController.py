import sqlite3

class DataBaseController:
	registeredEntities: dict
	
	def __init__(self, dataBaseName):
		self.dataBaseName = dataBaseName
		self.dbConnection = sqlite3.connect(dataBaseName)
		
	def registerEntity(self, entity):
		pass