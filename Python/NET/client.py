from socket import socket

s = socket()
s.connect(('localhost', 2000))

while 1:
	req = input(">")
	if req == "q":
		break
	s.send(bytes(req, "utf-8"))
	if req == "stop":
		break
