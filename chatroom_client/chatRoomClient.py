from socket import *
from sys import exit
import os
import struct
import time

serverName = '142.58.15.211'
serverPort = 42069

clientSock = socket(AF_INET, SOCK_STREAM)

try:
	clientSock.connect((serverName, serverPort))
except error as bruh:
	print(str(bruh))
	exit()

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

def main():
    

if __name__ == '__main__':
    main()