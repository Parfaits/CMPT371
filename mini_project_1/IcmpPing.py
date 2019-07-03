# The rest are from CMPT371 given by Ouldooz Baghban Karimi
# The '# Fill in start' to '# Fill in end' are my part

# Fill in start
# part 2
RTTList = []
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
		TTL = struct.unpack("i", recPacket[8:9])
		header = struct.unpack("bbHHh", recPacket[20:28]) # 20 to 28 because ICMP header starts at bits 160 (20 byte)
		# header is a tuple of (type, code, checksum, packet id, sequence)
		dataSize = struct.calcsize("d")
		data = struct.unpack("d", recPacket[28:28 + dataSize])
		print("PONG: ", header[0])
		RTT = data - timeReceived
		if header[3] == ID:
			return RTT
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
	while True :  
		delay = doOnePing(dest, timeout)
		# print(delay)
		# Fill in start
		# part 2
		RTTList.append(delay)
		# Fill in end
		time.sleep(1)# one second
	# return delay
	# Fill in start
	# part 2
	loss = 0
	goodRTT = []
	for x in RTTList:
		if x == "Request timed out.":
			loss += 1
		else:
			goodRTT.append(x)
	minRTT = min(goodRTT)
	maxRTT = max(goodRTT)
	try:
		avgRTT = sum(goodRTT)/len(goodRTT)
		lossPerc = round((loss/len(RTTList))*100)
	except ZeroDivisionError:
		print("Error: Divide by zero.")
	
	print("Min RTT: {}, Max RTT: {}, Avg RTT: {}, Loss rate percentage: {}".format(minRTT, maxRTT, avgRTT, lossPerc))
	# Fill in end