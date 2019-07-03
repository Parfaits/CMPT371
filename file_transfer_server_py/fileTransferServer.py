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

# Define file transfer protocol
def uploadToClient(Sock, fileName):
	with open(fileName, 'rb') as file:
		sendBytes = file.read(4026)
		Sock.send(sendBytes)
		# i = 1
		# case: file > than 4026 bytes
		while sendBytes != b'':
			sendBytes = file.read(4026)
			# i += 1
			# print("bytes sent: {} {} bytes".format(len(sendBytes), i))
			Sock.send(sendBytes)

def downloadFromClient(Sock, fileName, fileSize):
	newFile = open(fileName, 'wb')
	# Retrieve data
	fileData = Sock.recv(4026)
	totalBytes_received = len(fileData)
	newFile.write(fileData)
	while totalBytes_received < fileSize:
		fileData = Sock.recv(4026)
		totalBytes_received += len(fileData)
		newFile.write(fileData)
		print("{0:.2f}% Uploaded".format((float(totalBytes_received)/float(fileSize))*100))
	newFile.close()
# End file transfer protocol

def fileNameSystem(fileName, fileType):
	f = os.listdir()
	i = 1
	name = "{}{}".format(fileName, fileType)
	if name in f:
		name = "{} ({}){}".format(fileName, i, fileType)
		while name in f:
			i += 1
			name = "{} ({}){}".format(fileName, i, fileType)
	return name

def on_Client(clientSocket, addr):
	OPTION = ["download", "upload"]
	curDir = os.getcwd()
	f = os.listdir()
	f.remove(os.path.basename(__file__))
	while True:
		try:
			opt = recv_msg(clientSocket).decode()
			print("opt ", opt)
			if opt == OPTION[0]:
				print("Client wants to download. Send OK.")
				send_msg(clientSocket, "OK".encode())
				# Send client how many files are here
				numFiles = str(len(f)).encode()
				send_msg(clientSocket, numFiles)
				print("sent client number of files in archive: " + numFiles.decode())
				for x in f:
					# Send client the list of file names
					send_msg(clientSocket, x.encode())
					# print("sent file name: ", x)
				file_selected = recv_msg(clientSocket).decode()
				try:
					thisFile = f.index(file_selected)
				except ValueError as e:
					raise e
				# Send client file size
				thisFileSize = str(os.path.getsize(f[thisFile]))
				send_msg(clientSocket, thisFileSize.encode())
				uploadToClient(clientSocket, f[thisFile])
				# Signal client that download has finished

				print("File {} sent to client address {}.\nFile size: {} bytes".format(f[thisFile], addr, thisFileSize))
				clientSocket.close()
				break

			elif opt == OPTION[1]:
				print("Client wants to upload. Send READY.")
				send_msg(clientSocket, "READY".encode())
				# Get file size from client
				fileSize = int(recv_msg(clientSocket).decode())
				raw_fileName = recv_msg(clientSocket).decode()
				fileExtension = recv_msg(clientSocket).decode()
				fileName = fileNameSystem(raw_fileName, fileExtension)
				downloadFromClient(clientSocket, fileName, fileSize)
				# Signal file uploaded
				print("File {} uploaded from client address {}.\nFile size: {} bytes".format(fileName, addr, fileSize))
				clientSocket.close()
				break
			else:
				send_msg(clientSocket, "You idiot! Absolute baffoon.".encode())
				clientSocket.close()
				break
		except AttributeError as e:
			print("The client oofed.")
			# print(e)
			clientSocket.close()
			break
		




serverSock.listen(5)
print("Lezz GO!")
while True:
	connectionSocket, addr = serverSock.accept()
	print("Got the monies from ", addr)

	_thread.start_new_thread(on_Client, (connectionSocket, addr))
serverSock.close()