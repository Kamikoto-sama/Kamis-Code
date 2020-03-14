from threading import Thread
# from NET.server import Server
from sqlite3 import Connection

class ServerTerminal(Thread):
	commands: dict

	def __init__(self, server):
		super().__init__()
		self.dbProvider = server.dbProvider
		self.server = server
		self.bindCommands()

	def bindCommands(self):
		self.commands = {
			'stop': self.server.stop,
			'sql': self.runSql,
			'clients': self.listClients
		}
		
	def listClients(self):
		clients = self.server.clients
		print("Connected clients:" if len(clients) > 0 else "No clients connected")
		for client in clients:
			print(client.index, client.address, client.connectionTime)

	def runSql(self):
		db = self.dbProvider.getDbConnection()
		while 1:
			query = input("sql>")
			if query == "q":
				break
			self.executeSqlQuery(db, query)

	@staticmethod
	def executeSqlQuery(db: Connection, query):
		try:
			res = db.execute(query)
		except Exception as e:
			print(e)
			return
		if "select" == query[:6].lower():
			for row in list(res):
				print(row)
		else:
			db.commit()

	def run(self):
		while self.server.isWorking:
			command = input(">")
			if command == "":
				continue
			self.executeCommand(command)

	def executeCommand(self, command):
		try:
			commandName, *params = command.split()
			if commandName not in self.commands:
				print("Unknown command")
				return
			self.commands[commandName](*params)
		except Exception as e:
			print(e)
