from socket import socket
from json import JSONDecoder
from threading import Thread
from datetime import datetime
from models import ClientInfo, Request

dataClosingSequence = b"__"
dataPackageSize = 1024

class ClientHandler(Thread):
	def __init__(self, server, clientInfo: ClientInfo, clientIndex, dbConnection):
		super().__init__()
		self.server = server
		self.connection: socket = clientInfo.connection
		self.clientAddress = clientInfo.fullAddress 
		self.clientIndex = clientIndex
		self.connectionTime = datetime.now().strftime("%H:%M:%S")
		self.clientRole = None
		self.dbConnection = dbConnection
		self.clientController = None
		
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

	def handleRequest(self, rawRequest):
		rawRequest = rawRequest[:-len(dataClosingSequence)]
		print(f"Client {self.clientIndex} {self.clientAddress} requested {rawRequest}")
		
		request = self.deserializeRequest(rawRequest)
		
	@staticmethod
	def deserializeRequest(rawRequest):
		requestDict = JSONDecoder().decode(rawRequest)
		return Request(**requestDict)

	def respond(self, data: str):
		data = data.encode("utf-8")
		self.connection.send(data)