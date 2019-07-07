# The rest are from CMPT371 given by Ouldooz Baghban Karimi
# The '# Fill in start' to '# Fill in end' are my part

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