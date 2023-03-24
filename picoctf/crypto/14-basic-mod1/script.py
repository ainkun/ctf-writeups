cipher = [91,322,57,124,40,406,272,147,239,285,353,272,77,110,296,262,299,323,255,337,150,102]
character_set = 'abcdefghijklmnopqrstuvwxyz0123456789_'

flag = ''


for c in cipher:
	n = c % 37
	flag = flag + character_set[n]

print('picoCTF{'+flag+'}')