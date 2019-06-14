from socket import *
from sys import exit

serverName = '0.0.0.0'
serverPort = 1696

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
try:
	serverSock.bind((serverName, serverPort))
except error as bruh:
	print(str(bruh))
	exit()

serverSock.listen(5)
print("The swag dealer is ready, gibe me the memes.")
while True:
	connectionSocket, addr = serverSock.accept()
	print("Got the monies from ", addr)

	data = connectionSocket.recv(1024).decode()
	print("I got the: ", data)
	connectionSocket.send("Get scammed bro #dab.".encode())

	connectionSocket.close()