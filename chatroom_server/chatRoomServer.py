from socket import *
from sys import exit
import os
import _thread
import struct

serverName = '0.0.0.0'
serverPort = 42069

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
try:
	serverSock.bind((serverName, serverPort))
except error as bruh:
	print(str(bruh))
	exit()

usernames = {}
clients = []
clientAddress = []

# Define message protocol
def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
# End message protocol

def reconnect():
    

def chatLobby(sock1, sock2, addr1, addr2):
    msg = recv_msg(sock).decode()
    if msg == 'q'
        sock.close()
        break
    elif len(msg) > 0:
        send_msg(sock, msg.encode())
    print("(Log {}) {}".format(addr, msg))

def ():
    for x in clients:
        try:
            
        except Exception as e:
            raise e

def list():
    ls = ''
        

def shell():
    cmd = input('>').lower()
    if cmd == "list":
        
    elif cmd in "kick "

    elif cmd in "ban "

    elif cmd in "accept "

    elif cmd == "decline"

    elif cmd in "invite "

    else:
        print("Wtf?")

def on_Client(clientSocket, addr):
	

serverSock.listen(5)
print("Lezz GO!")
while True:
    try:
    	connectionSocket, addr = serverSock.accept()
        serverSock.setblocking(1)
    	print("Got the monies from ", addr)
        name = recv_msg(connectionSocket).decode()
        print("Username is ", name)
        usernames[name] = 

        clients.append(connectionSocket)
        clientAddress.append(addr)
    except:
        print("Not accepting.")

	_thread.start_new_thread(on_Client, (connectionSocket, addr))
serverSock.close()