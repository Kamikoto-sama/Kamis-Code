import socket as Socket

from server import port, address

socket = Socket.socket()
socket.connect((address, port))