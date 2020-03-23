import socket as Socket
from threading import Thread
from clientHandler import ClientHandler
from dbProvider import DataBaseProvider
from models import ClientInfo
from serverTerminal import ServerTerminal

class Server:
	def __init__(self, address="", port=2000, dbProvider=DataBaseProvider()):
		self.socket = Socket.socket()
		self.socket.bind((address, port))
		
		self.__isWorking = False
		self.dbProvider = dbProvider
		self.clients = {}

	@property
	def isWorking(self):
		return self.__isWorking

	def start(self):
		self.__isWorking = True
		Thread(target=self.listenClients).start()
		ServerTerminal(self).start()
		
	def listenClients(self):
		while self.__isWorking:
			self.socket.listen()
			clientInfo = self.waitClientConnection()
			if not self.__isWorking:
				return

			clientIndex = len(self.clients)
			clientDbConnection = self.dbProvider.getDbConnection()
			clientHandler = ClientHandler(self, clientInfo, clientIndex, clientDbConnection)
			self.clients[clientIndex] = clientHandler
			clientHandler.start()
			
			print(f"\r{clientHandler.clientAddress} has connected")
	
	def waitClientConnection(self):
		try:
			clientInfo = self.socket.accept()
			return ClientInfo(clientInfo)
		except OSError:
			if self.__isWorking:
				raise
		
	def onClientDisconnected(self, client: ClientHandler):
		self.clients.pop(client.clientIndex)
		print(f"\r{client.clientIndex} {client.clientAddress} has disconnected")

	def stop(self):
		self.__isWorking = False
		self.socket.close()
		for client in self.clients.values():
			client.disconnect()
		print("Server has stopped")

if __name__ == '__main__':
	Server().start()