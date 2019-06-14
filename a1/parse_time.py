import math
T = []
num = []

def read_milliseconds(FILE):
	with open('%s' % (FILE), 'r') as infile:
		for line in infile:
			T = line.split()
			for i in range(len(T)):
				if T[i] == "ms":
					# print(T[i-1])
					# num[j] = float(T[i-1])
					num.append(float(T[i-1]))

def get_col(col):
	i = col
	A = []
	while i < len(num):
		A.append(num[i])
		i+=3
	# print(A)
	return A

def mean(A):
	m = sum(A)
	# print(m)
	n = len(A)
	m = m/n
	return m

def standard_deviation(A, mean):
	L = []
	for i in range(len(A)):
		L.append((A[i]-mean)**2)
	# print(L)
	x = sum(L)
	n = len(L)
	x = math.sqrt(x/n)
	return x

def max_delay(A):
	return max(A)

def main():
	RTT = [0, 0, 0]
	# FILE = input("Text file: ")
	read_milliseconds("trace_utoronto_3.txt")
	a = get_col(0)
	b = get_col(1)
	c = get_col(2)
	RTT[0] = sum(a)
	RTT[1] = sum(b)
	RTT[2] = sum(c)
	M = mean(RTT)
	SD = standard_deviation(RTT, M)
	# MAX = max_delay()
	# print(num)
	# print(a)
	print("Col 0: {}, col 1: {}, col 2: {}".format(RTT[0], RTT[1], RTT[2]))
	print("swag: ", M)
	print("Hell YEA: ", SD)
	# print("THICCC ", MAX)

if __name__ == '__main__':
	main()
