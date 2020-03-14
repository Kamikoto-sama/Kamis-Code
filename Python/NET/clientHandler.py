from datetime import datetime
from threading import Thread
from socket import socket

dataClosingSequence = b"__"

class ClientHandler(Thread):
	def __init__(self, server, clientInfo, index):
		super().__init__()
		self.server = server
		self.connection, self.rawAddress = clientInfo
		self.address = f"{self.rawAddress[0]}:{self.rawAddress[1]}"
		self.index = index
		self.connectionTime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
		self.connected = True
		
	def run(self):
		connection: socket = self.connection
		requestParts = []
		while self.connected and (receivedData := connection.recv(1024)):
			requestParts.append(receivedData.decode('utf-8'))
			if receivedData.endswith(dataClosingSequence):
				self.handleRequest(''.join(requestParts))
				requestParts = []
		self.server.onClientDisconnected(self)
		
	def handleRequest(self, request):
		request = request[:-len(dataClosingSequence)]
		print(request if len(request) < 20 else len(request))
		