from socket import socket
from threading import Thread

s = socket()
s.bind(('', 2000))

class ServerState:
	isWorking:bool = True

def stopServer(serverState: ServerState):
	serverState.isWorking = False
	s.close()

def listenClient(connection, clientAddress, serverState):
	clientAddress = f'{clientAddress[0]}:{clientAddress[1]}'
	print("connected:", clientAddress)
	while receivedData := connection.recv(1024):
		if receivedData.decode('utf-8') == "stop":
			stopServer(serverState)
			break
		print(f'{clientAddress} sent:', receivedData)
	connection.close()
	print("disconnected:", clientAddress)

def startServer():
	state = ServerState()
	print("Waiting for clients...")
	while state.isWorking:
		s.listen()
		client = s.accept()
		Thread(target=listenClient, args=(*client, state)).start()

if __name__ == '__main__':
	startServer()