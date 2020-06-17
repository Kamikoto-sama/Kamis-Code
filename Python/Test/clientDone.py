import socket as Socket

from server import port, address, dataPackageSize, encoding, closingSequence

socket = Socket.socket()
socket.connect((address, port))

while 1:
	message = input(">")
	if message == "q":
		break
	socket.sendall(message.encode(encoding) + closingSequence)
	response = socket.recv(dataPackageSize)
	print(response.decode(encoding))
socket.close()