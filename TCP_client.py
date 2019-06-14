from socket import *
from sys import exit

serverName = ''
serverPort = 1420

clientSock = socket(AF_INET, SOCK_STREAM)

try:
	clientSock.connect((serverName, serverPort))
except error as bruh:
	print(str(bruh))
	exit()

data = input("Moneis plzzz: ")
clientSock.send(data.encode())
recieved_data = clientSock.recv(1024).decode()
print("(From server) {}\nI got scammed".format(recieved_data))

clientSock.close()