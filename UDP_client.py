from socket import *
from sys import exit

serverName = ''
serverPort = 6969

clientSock = socket(AF_INET, SOCK_DGRAM)

data = input("Moneis plzzz: ")
clientSock.sendto(data.encode(), (serverName, serverPort))
print("Sent.")
recieved_data, Addr = clientSock.recvfrom(1024)
print("(From server) {}\nI got scammed".format(recieved_data.decode()))

clientSock.close()