import socket as Socket
from threading import Thread
from serverTerminal import ServerTerminal
from dbProvider import DataBaseProvider
from clientHandler import ClientHandler


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
			clientHandler = ClientHandler(self, clientInfo, clientIndex, self.dbProvider)
			self.clients[clientIndex] = clientHandler
			clientHandler.start()
			print(f"\r{clientHandler.address} has connected")
	
	def waitClientConnection(self):
		try:
			return self.socket.accept()
		except OSError:
			if self.__isWorking:
				raise
		
	def onClientDisconnected(self, client: ClientHandler):
		self.clients.pop(client.index)
		print(f"\r{client.index} {client.address} has disconnected")

	def stop(self):
		self.__isWorking = False
		self.socket.close()
		for client in self.clients.values():
			client.disconnect()
		print("Server has stopped")

if __name__ == '__main__':
	Server().start()