import socket as Socket

address = "localhost"
port = 2000
dataPackageSize = 1024
closingSequence = b"\r\n\r\n"
encoding = "utf-8"

def getDataPackage(connection):
	try:
		dataBytes = connection.recv(dataPackageSize)
		return dataBytes
	except ConnectionError:
		return 0

def listenClient(connection, clientAddress):
	dataParts = []
	while dataBytes := getDataPackage(connection):
		dataParts.append(dataBytes.decode(encoding))
		if not dataBytes.endswith(closingSequence):
			continue
		data = "".join(dataParts)[:-len(closingSequence)]
		print(data)
		connection.sendall(f"you've requested: {data}".encode(encoding))
		dataParts.clear()
	print(f"Client {clientAddress} has disconnected")

def startServer():
	socket = Socket.socket()
	socket.bind((address, port))
	socket.listen()

	while True:
		try:
			connection, clientAddress = socket.accept()
			print(f"{clientAddress} has connected")
			listenClient(connection, clientAddress)
		except OSError:
			break
	print("Server has stopped")
	
if __name__ == '__main__':
	startServer()