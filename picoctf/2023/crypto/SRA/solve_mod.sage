e = 65537
d = 2374924730695331980666696108116881030499766801250410405192548099790203981209
ct = 24061514671443903391690548449273614205558035441569029488091015203490263562130

phi = (e*d)-1

list = []
for a,b in factor(phi):
	for _ in range(b):
		list.append(a)

primes = []

print("factoing primes using combinations")
for i in range(len(list)):
	for comb in Combinations(list,i):
		prod = product(comb)
		if is_prime(prod + 1):
			prime = prod + 1
			if prime.nbits() == 128:
				primes.append(prime)

print(primes)
print("decrypting cipher")

for vals in Combinations(primes):
	n = product(vals)
	try:
		m = bytes.fromhex(hex(pow(ct,d,n))[2:]).decode()
		if m.isalnum():
			print(m)
			break
	except:
		pass