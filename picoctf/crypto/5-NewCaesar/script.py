import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

enc_flag = 'ihjghbjgjhfbhbfcfjflfjiifdfgffihfeigidfligigffihfjfhfhfhigfjfffjfeihihfdieieih'

flag = ''

def b16_decode(cipher):
	dec = ""
	for i in range(int(len(cipher)/2)):
		char = cipher[i*2:(i*2)+2]
		num1 = ALPHABET.index(char[0])
		num2 = ALPHABET.index(char[1])
		bina = "{0:04b}".format(num1)+"{0:04b}".format(num2)
		dec += chr(int(bina,2))
	return dec


def unshift(c, k):
    t1 = ord(c) - LOWERCASE_OFFSET
    t2 = ord(k) - LOWERCASE_OFFSET
    return ALPHABET[(t1 - t2) % 16]


'''
for k in ALPHABET:
	dec = ''
	keyloc = ALPHABET.index(k)
	for i in enc_flag:
		loc = ALPHABET.index(i)
		if (keyloc<=loc):
			dec += chr(loc-keyloc+97)
		else:
			dec += chr(loc-keyloc+16+97)
	print(str(k)+": "+b16_decode(dec))

'''
for k in ALPHABET:
	dec = ''
	for c in enc_flag:
		dec += unshift(c,k)
	flag = b16_decode(dec)
	print(flag)

