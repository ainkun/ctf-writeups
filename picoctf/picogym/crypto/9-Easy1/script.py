import string

ENC_FLAG = "UFJKXQZQUNB"
KEY = "SOLVECRYPTO"
ENC_LEN = len(ENC_FLAG)
K_LEN = len(KEY)
ALPHA = string.ascii_uppercase

DEC_FLAG = ""

for i in range(ENC_LEN):
		if ENC_FLAG[i] in ALPHA:
			e_num = ALPHA.index(ENC_FLAG[i])
			k_num = ALPHA.index(KEY[i%K_LEN])
			dec = ALPHA[(e_num - k_num)%26]
			DEC_FLAG = DEC_FLAG + dec
		else:
			DEC_FLAG = DEC_FLAG + ENC_FLAG[i]

print("picoCTF{" + DEC_FLAG + "}")