enc = "!?}De!e3d_5n_nipaOw_3eTR3bt4{_THB"

flag = ''

for i in range(0, len(enc), 3):
	flag += enc[i+2]
	flag += enc[i]
	flag += enc[i+1]

print(flag[::-1])


