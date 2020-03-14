import datetime
import socket as Socket
from threading import Thread
from serverTerminal import ServerTerminal
from dbProvider import DataBaseProvider
from clientHandler import ClientHandler


class Server:
	def __init__(self, address="", port=2000, dbProvider=DataBaseProvider()):
		self.address = address
		self.port = port
		self.socket = Socket.socket()
		self.socket.bind((address, port))
		self.__isWorking = False
		self.dbProvider = dbProvider
		self.clients = []

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
			
			clientHandler = ClientHandler(self, clientInfo, len(self.clients))
			self.clients.append(clientHandler)
			clientHandler.start()
			print(f"\r{clientHandler.address} has connected")
	
	def waitClientConnection(self):
		try:
			clientInfo = self.socket.accept()
			return clientInfo
		except OSError:
			if self.__isWorking:
				raise
			return None, None
		
	def onClientDisconnected(self, client: ClientHandler):
		self.clients.remove(client)
		print(f"\r{client.index} {client.address} has disconnected")

	def stop(self):
		self.__isWorking = False
		self.socket.close()
		
		print("Server has stopped")

if __name__ == '__main__':
	Server().start()