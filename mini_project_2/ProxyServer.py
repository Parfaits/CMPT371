from socket import *
import sys

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)
	
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start
# print(sys.argv)
server_ip = sys.argv[1]
serverPort = 42069
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
try:
	tcpSerSock.bind((server_ip, serverPort))
except error as e:
	raise e
tcpSerSock.listen(5)
# Fill in end

while 1:
	# Strat receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
    		  # Fill in start
	# data = b''
	# while True:
	# 	data += tcpCliSock.recv(1024)
	# 	if not data:
	# 		break
	# message = data.decode()
	message = tcpCliSock.recv(1024)
	print("message len: ", len(message))
              # Fill in End
	print(message)
	# Extract the filename from the given message
	print(message.split()[1])
	filename = message.split()[1].partition("/")[2]
	print(filename)
	fileExist = "false"
	filetouse = "/" + filename
	print(filetouse)
	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "r")        
		outputdata = f.readlines()                        
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.0 200 OK\r\n")            
		tcpCliSock.send("Content-Type:text/html\r\n")
        # Fill in start
		# contentLength = 0
		# for x in range(len(outputdata)):
		# 	contentLength += len(outputdata[x])
		# tcpCliSock.send("Content-Length: {}".format(contentLength))
		# message = ""
		# for i in outputdata:
		# 	message += i
		# tcpCliSock.send(message)
		for x in outputdata:
			tcpCliSock.send(x)
		f.close()
        # Fill in end
		print('Read from cache')   
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false": 
			# Create a socket on the proxyserver
                # Fill in start
			c = socket(AF_INET, SOCK_STREAM)
                # Fill in end
			hostn = filename.replace("www.","",1)         
			print(hostn)                                   
			try:
				# Connect to the socket to port 80
                # Fill in start
				# webServerIP = hostn.split('/')[2]
				# print(webServerIP)
				# urlPos = hostn.find('/', 1)
				
				# print("BRUHHHH ", hostn)
				webServerPort = 80
				# print("WHYYYYYYYYYYYYYYYYYYYYY")
				c.connect((hostn, webServerPort))
				print("Got connection.")
                # Fill in end
				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				fileobj = c.makefile('r', 0)             
				fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")  
				# Read the response into buffer
                # Fill in start
				response = fileobj.readlines()
                # Fill in end
				# Create a new file in the cache for the requested file. Also send the response in the buffer to client socket and the corresponding file in the cache
				tmpFile = open("./" + filename,"wb")  
                # Fill in start
				# print("KMS")
				# tmpFile.write(response)
				# tmpFile.close()
				# c.close()
				# responseCode = response[0].split()[1]
				# responseMessage = response[0].split()[2]
				# if responseCode == "200":
				# 	for n in response:
				# 		tmpFile.write(n)
				# 		tcpCliSock.send(n)
				# else:
				# 	# print("response: {}".format(''.join(response)))
				# 	raise Exception("Non 200 response code. Details:\n{}".format(response))
				for n in response:
					tmpFile.write(n)
					tcpCliSock.send(n)
				tmpFile.close()
                # Fill in end
			# except Exception as e:
			# 	raise e
			except:
				print("Illegal request")
		else:
			# HTTP response message for file not found
            # Fill in start
			# tcpCliSock.send("HTTP/1.0 404 File Not Found\r\n")
			# tcpCliSock.send("Content-Type:text/html\r\n")
			# tcpCliSock.send("\r\n")
			print("HTTP/1.0 404 File Not Found\r\n")
			print("Content-Type:text/html\r\n")
			print("\r\n")
            # Fill in end
	# Close the client and the server sockets    
	tcpCliSock.close() 
# Fill in start
tcpSerSock.close()
# Fill in end
