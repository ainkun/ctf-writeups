import string

charac = string.ascii_lowercase

cipher = [16,9,3,15,3,20,6,'{',20,8,5,14,21,13,2,5,18,19,13,1,19,15,14,'}']

flag = ''

for num in cipher:
	if type(num) == int:
		flag = flag + charac[num-1]
	else:
		flag = flag + num

print(flag)
