from socket import *
from sys import exit

serverName = '0.0.0.0'
serverPort = 6969

serverSock = socket(AF_INET, SOCK_DGRAM)
serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
try:
	serverSock.bind((serverName, serverPort))
except error as bruh:
	print(str(bruh))
	exit()

print("The swag dealer is ready, gibe me the memes.")
while True:
	data, Addr = serverSock.recvfrom(1024)
	print("I got the {} from {}.".format(data.decode(), Addr))
	serverSock.sendto("Get scammed bro #dab.".encode(), Addr)
