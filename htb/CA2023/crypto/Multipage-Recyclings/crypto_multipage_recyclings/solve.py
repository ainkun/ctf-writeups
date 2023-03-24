
def blockify(message, size):
	return [message[i:i + size] for i in range(0, len(message), size)]

def xor(a, b):
	return b''.join([bytes([_a ^ _b]) for _a, _b in zip(a, b)])

ct = "bc9bc77a809b7f618522d36ef7765e1cad359eef39f0eaa5dc5d85f3ab249e788c9bc36e11d72eee281d1a645027bd96a363c0e24efc6b5caa552b2df4979a5ad41e405576d415a5272ba730e27c593eb2c725031a52b7aa92df4c4e26f116c631630b5d23f11775804a688e5e4d5624"
r = 3
phrases = ['8b6973611d8b62941043f85cd1483244', 'cf8f71416111f1e8cdee791151c222ad']


ct = blockify(bytes.fromhex(ct),16)

print(xor(ct[r+1], bytes.fromhex(phrases[0])))
print(xor(ct[r+2], bytes.fromhex(phrases[1])))