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

# Define file transfer protocol
def downloadFromServer(Sock, fileName, fileSize):
	timeStamp = time.strftime("-%Y-%b-%d__%H_%M_%S.",time.localtime())
	splicedFileName = fileName.split('.')
	fileName_with_timeStamp = timeStamp.join(splicedFileName)
	newFile = open(fileName_with_timeStamp, 'wb')
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

def uploadToServer(Sock, fileName):
	with open(fileName, 'rb') as file:
		sendBytes = file.read(4026)
		clientSock.send(sendBytes)
		# case: file > than 4026 bytes
		while sendBytes != b'':
			sendBytes = file.read(4026)
			clientSock.send(sendBytes)
# End file transfer protocol

def quicksearch_File(fileNickName, fileList=None):
	f = os.listdir()
	if fileList == None:
		duplicateList = [x for i,x in enumerate(f) if x.startswith(fileNickName)]
		return duplicateList
	else:
		duplicateList = [x for i,x in enumerate(fileList) if x.startswith(fileNickName)]
		return duplicateList

def stupid_User_Loop(Sock, fileName, fileList, listLen, fileNameList=None):
	fileSelectedList = fileList
	user_Interrogated = fileName
	l = listLen
	if fileNameList:
		fileSelectedList = quicksearch_File(user_Interrogated, fileNameList)
	else:
		fileSelectedList = quicksearch_File(user_Interrogated)
	while (user_Interrogated not in fileSelectedList) and l != 1 and user_Interrogated != 'q':
		print("Wtf?")
		print(fileSelectedList)
		user_Interrogated = input("Which one bruh?\n>")
		if fileNameList:
			fileSelectedList = quicksearch_File(user_Interrogated, fileNameList)
		else:
			fileSelectedList = quicksearch_File(user_Interrogated)
		l = len(fileSelectedList)
	if user_Interrogated == 'q':
		Sock.close()
		exit()
	return fileSelectedList[0]

def main():
	OPTION = input("Want to download or upload?\n>").lower()
	while (OPTION != 'q') and not OPTION.startswith('u') and not OPTION.startswith('d'):
		OPTION = input("Bruh what?\n>").lower()

	if OPTION == 'q':
		send_msg(clientSock, 'q'.encode())
		clientSock.close()
		exit()
	elif OPTION.startswith('d'):
		send_msg(clientSock, "download".encode())
		print("I'll have two number 9's, a number 9 large, a number 6 with extra dip, a number 7, two number 45's, one with cheese, and a large soda.﻿")
		conf = recv_msg(clientSock).decode()
		print("(server) ", conf)
		if conf == "OK":
			numFiles = int(recv_msg(clientSock).decode())
			print("There are {} files to choose. Here is a list:".format(numFiles))
			fileNameList = []
			for x in range(numFiles):
				fileNameList.append(recv_msg(clientSock).decode())
			print(fileNameList)
			fileName = input("What file you want?\n>")
			if fileName == 'q':
				clientSock.close()
				exit()
			fileMatches = quicksearch_File(fileName, fileNameList)
			numFilesMatch = len(fileMatches)
			if numFilesMatch != 1:
				fileSelected = stupid_User_Loop(clientSock, fileName, fileMatches, numFilesMatch, fileNameList)
			else:
				fileSelected = fileMatches[0]

			send_msg(clientSock, fileSelected.encode())
			# Server sent file size
			fileSize = int(recv_msg(clientSock).decode())
			print("What's the size?")
			print("(server) It's this big: {} bytes".format(fileSize))
			# Retrieve data
			downloadFromServer(clientSock, fileSelected, fileSize)
			# Signal file uploaded
			print("Here's the meme, ez clap.")
			print("File {} download to: {}".format(fileSelected, os.getcwd()) )
			clientSock.close()
		else:
			print("AYOO WTF!!!???")
			clientSock.close()
			exit()
	elif OPTION.startswith('u'):
		send_msg(clientSock, "upload".encode())
		print("Upload memes.")
		conf = recv_msg(clientSock).decode()
		if conf == "READY":
			f = os.listdir()
			f.remove(os.path.basename(__file__))
			# f.remove("kill_pid_on_port.sh")
			print(f)
			fileToSend = input("What meme to sacrifice??\n>")
			if fileToSend == 'q':
				clientSock.close()
				exit()
			fileMatches = quicksearch_File(fileToSend)
			numFilesMatch = len(fileMatches)
			if numFilesMatch != 1:
				fileSelected = stupid_User_Loop(clientSock, fileToSend, fileMatches, numFilesMatch)
			else:
				fileSelected = fileMatches[0]
			fileName, fileExtension = os.path.splitext(fileSelected)
			fileToSend_Size = str(os.path.getsize(fileSelected))
			send_msg(clientSock, fileToSend_Size.encode())
			send_msg(clientSock, fileName.encode())
			send_msg(clientSock, fileExtension.encode())
			uploadToServer(clientSock, fileSelected)
			print("File {} sent to server.".format(fileSelected))
			clientSock.close()
		else:
			print("BRUH")
			clientSock.close()
			exit()
	else:
		wtf = recv_msg(clientSock).decode()
		print(wtf)
		clientSock.close()
		exit()

if __name__ == "__main__":
	main()