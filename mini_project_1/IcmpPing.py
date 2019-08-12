from socket import *
import os
import sys
import struct
import time
import select
import binascii  

ICMP_ECHO_REQUEST = 8

# ====================== READ ME ======================
# The rest are given by Ouldooz Baghban Karimi
# The '# Fill in start' to '# Fill in end' are my part
# ====================== READ ME ======================

# Fill in start
# part 2
RTTList = []
# Fill in end

# Fill in start
# part 3
errorDict = {3: {0: "Destination network unreachable", 1: "Destination host unreachable", 2: "Destination protocol unreachable",3: "Destination port unreachable", 4: "	Fragmentation required, and DF flag set", 5: "Source route failed", 6: "Destination network unknown",7: "Destination host unknown",8: "Source host isolated",9: "Network administratively prohibited",10: "Host administratively prohibited",11: "Network unreachable for ToS",12: "Host unreachable for ToS",13: "Communication administratively prohibited",14: "Host Precedence Violation",15: "Precedence cutoff in effect"},
			5: {0: "Redirect Datagram for the Network", 1: "Redirect Datagram for the Host",2: "Redirect Datagram for the ToS & network",3: "Redirect Datagram for the ToS & host"},
			11: {0: "TTL expired in transit", 1: "Fragment reassembly time exceeded"},
			12: {0: "Pointer indicates the error",1: "Missing a required option", 2: "Bad length"}
			}
# Fill in end

def checksum(string): 
	csum = 0
	countTo = (len(string) // 2) * 2  
	count = 0

	while count < countTo:
		thisVal = ord(string[count+1]) * 256 + ord(string[count]) 
		csum = csum + thisVal 
		csum = csum & 0xffffffff  
		count = count + 2
	
	if countTo < len(string):
		csum = csum + ord(string[len(string) - 1])
		csum = csum & 0xffffffff 
	
	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum 
	answer = answer & 0xffff 
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer 
	
def receiveOnePing(mySocket, ID, timeout, destAddr):
	timeLeft = timeout
	
	while 1: 
		startedSelect = time.time()
		whatReady = select.select([mySocket], [], [], timeLeft)
		howLongInSelect = (time.time() - startedSelect)
		if whatReady[0] == []: # Timeout
			return "Request timed out."
	
		timeReceived = time.time() 
		recPacket, addr = mySocket.recvfrom(1024)
		
		# Fill in start
		# part 1 and 3
		TTL = struct.unpack("B", recPacket[8:9])[0] # TTL in the IP header 8 octets down and is only of size 1 octet
		header = struct.unpack("bbHHh", recPacket[20:28]) # 20 to 28 because ICMP header starts at bits 160 (20 byte)
		# header is a tuple of (type, code, checksum, packet id, sequence)
		if header[0] == 0:
			data = struct.unpack("d", recPacket[28:])[0]
			RTT = (1000*timeReceived) - (float(data)*1000)
		else:
			try:
				errorMessage = errorDict[header[0]][header[1]]
			except KeyError:
				print("Error message not implemented.")
				sys.exit()
		# print("PONG: ", header)
		# print("data: {}, timeReceived: {}".format(data, timeReceived))
		# print("TTL: ", TTL)
		# print("packet id: {}, ID: {}".format(header[3], ID))
		if header[0] == 0:
			if header[3] == ID:
				dataSize = len(recPacket[28:])
				sourceAddr = inet_ntoa(recPacket[12:16]) # convert int to ip string
				print("{} bytes from {}: icmp_seq={} ttl={} time={} ms".format(dataSize, sourceAddr, header[4], TTL, RTT))
				return RTT
		else:
			# print("Type: ", header[0])
			print("{}: {}".format(header[1], errorMessage))
			return ''
		# Fill in end
		
		timeLeft = timeLeft - howLongInSelect
		if timeLeft <= 0:
			return "Request timed out."

	
def sendOnePing(mySocket, destAddr, ID):
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)
	
	myChecksum = 0
	# Make a dummy header with a 0 checksum
	# struct -- Interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	# Calculate the checksum on the data and the dummy header.

	myChecksum = checksum(str(header + data)) 
	
	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
		# Convert 16-bit integers from host to network byte order
		myChecksum = htons(myChecksum) & 0xffff		
	else:
		myChecksum = htons(myChecksum)
		
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data
	
	mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.
	
def doOnePing(destAddr, timeout): 
	icmp = getprotobyname("icmp")

	# SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw
	mySocket = socket(AF_INET, SOCK_RAW, icmp)
	
	myID = os.getpid() & 0xFFFF  # Return the current process i
	sendOnePing(mySocket, destAddr, myID)
	delay = receiveOnePing(mySocket, myID, timeout, destAddr)
	
	mySocket.close()
	return delay
	
def ping(host, timeout=1):
	# timeout=1 means: If one second goes by without a reply from the server,
	# the client assumes that either the client's ping or the server's pong is lost
	dest = gethostbyname(host)
	print("Pinging " + dest + " using Python:")
	print("")
	# Send ping requests to a server separated by approximately one second
	# Fill in start
	# my SIGINT handler
	try:
		while True :  
			delay = doOnePing(dest, timeout)
			# print(delay)
			# Fill in start
			# part 2
			if type(delay) is str:
				print(delay)
			RTTList.append(delay)
			# Fill in end
			time.sleep(1)# one second
	except KeyboardInterrupt:

		# return delay
		# Fill in start
		# part 2
		loss = 0
		goodRTT = []
		for x in RTTList:
			if type(x) is float:
				goodRTT.append(x)
			else:
				loss += 1
		if len(goodRTT) == 0:
			# Case: every packet recieved is a error (non zero ICMP type)
			print("loss rate percentage: {}%".format(100))
			sys.exit()
		minRTT = min(goodRTT)
		maxRTT = max(goodRTT)
		avgRTT = sum(goodRTT)/len(goodRTT)
		lossPerc = round((loss/len(RTTList))*100)
		print("Statistics:")
		print("Min RTT: {} ms, Max RTT: {} ms, Avg RTT: {} ms, Loss rate percentage: {}%".format(minRTT, maxRTT, avgRTT, lossPerc))
		sys.exit()
		# Fill in end
	# Fill in end

# Bunch of ip addresses to test
# ping("google.com")
# ping("127.0.0.1")
# ping("192.168.1.134")
# ping("131.255.7.26") # South America: Buenos Aires (Argentina)
# ping("195.201.213.247") # Europe: Frankfurt (Germany)
# ping("110.50.243.6") # Asia: Tokyo (Japan)
ping("101.0.86.43") # Australia: Sydney
