from sqlite3 import Connection
from threading import Thread

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
			'clients': self.listClients,
			'disconnect': self.disconnectClient,
			'commands': self.showCommands,
			'send': self.sendMessageToClient,
		}
		
	def sendMessageToClient(self, clientIndex, *message):
		client = self.getClient(clientIndex)
		if client is None:
			return 
		client.respond(' '.join(message))
		
	def disconnectClient(self, clientIndex):
		client = self.getClient(clientIndex)
		if client is None:
			return 
		client.disconnect()
	
	def getClient(self, clientIndex):
		clientIndex = int(clientIndex)
		if not clientIndex in self.server.clients:
			print(f"No such client {clientIndex}")
			return
		return self.server.clients[clientIndex]
		
	def showCommands(self):
		print("Supported commands:")
		for command in self.commands:
			print(command)
		
	def listClients(self):
		clients = self.server.clients.values()
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
		if query[:6].lower() in ["select", "pragma"]:
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
