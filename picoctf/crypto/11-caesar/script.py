import string

CIPHER = "dspttjohuifsvcjdpoabrkttds"
ALPHA = string.ascii_lowercase
for i in range(26):
	DEC_flag = ""
	for cha in CIPHER:
		new = ALPHA[(ALPHA.index(cha) + i) % 26]
		DEC_flag = DEC_flag + new
	print(DEC_flag)