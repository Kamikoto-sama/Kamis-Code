from socket import socket
from threading import Thread
from datetime import datetime
from dbProvider import DataBaseProvider

dataClosingSequence = b"__"
dataPackageSize = 1024

class ClientHandler(Thread):
	def __init__(self, server, clientInfo, index, dbProvider: DataBaseProvider):
		super().__init__()
		self.dbProvider = dbProvider
		self.server = server
		self.connection: socket = clientInfo[0]
		self.rawAddress = clientInfo[1]
		self.address = f"{self.rawAddress[0]}:{self.rawAddress[1]}"
		self.index = index
		self.connectionTime = datetime.now().strftime("%H:%M:%S")
		
	def disconnect(self):
		self.connection.close()
		
	def run(self):
		requestParts = []
		while receivedData := self.getDataPackage():
			requestParts.append(receivedData.decode('utf-8'))
			if receivedData.endswith(dataClosingSequence):
				self.handleRequest(''.join(requestParts))
				requestParts = []
		if self.server.isWorking:
			self.server.onClientDisconnected(self)
		
	def getDataPackage(self):
		try:
			return self.connection.recv(dataPackageSize)
		except ConnectionAbortedError:
			return 0

	def handleRequest(self, request):
		request = request[:-len(dataClosingSequence)]
		print(request if len(request) < 20 else len(request))
		
	def respond(self, data: bytes):
		self.connection.send(data)