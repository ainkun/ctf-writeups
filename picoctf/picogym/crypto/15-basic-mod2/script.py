cipher = [104,85,69,354,344,50,149,65,187,420,77,127,385,318,133,72,206,236,206,83,342,206,370]
character_set = 'abcdefghijklmnopqrstuvwxyz0123456789_'

flag = ''

for c in cipher:
	n = c%41
	inverse = pow(n,-1,41)
	print(inverse)
	flag = flag + character_set[inverse-1]

print('picoCTF{'+flag+'}')