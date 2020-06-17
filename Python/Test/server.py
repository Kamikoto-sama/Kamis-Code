import socket as Socket

address = "localhost"
port = 2000
dataPackageSize = 10
dataClosingSequence = b"\r\n\r\n"
encoding = "utf-8"

def listenClients(connection, clientAddress):
	dataParts = []
	while 1:
		try:
			dataBytes = connection.recv(dataPackageSize)
		except ConnectionError:
			break
		if not dataBytes:
			break
		dataParts.append(dataBytes.decode(encoding))
		if not dataBytes.endswith(dataClosingSequence):
			continue
		data = "".join(dataParts)[:-len(dataClosingSequence)]
		dataParts.clear()
		print(len(data), data.encode(encoding))
	print(f"{clientAddress} has disconnected")

def startServer():
	socket = Socket.socket()
	socket.bind((address, port))
	socket.listen()
	
	while True:
		try:
			connection, clientAddress = socket.accept()
		except OSError:
			break
		print(f"{clientAddress} has connected")
		listenClients(connection, clientAddress)

	socket.close()
	print("Server has stopped")
	
if __name__ == '__main__':
	startServer()