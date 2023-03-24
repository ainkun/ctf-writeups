from pwn import *


'''
Results
---
All results are rounded
to 2 digits after the point.
ex. 9.5752 -> 9.58

Error Codes
---
* Divide by 0:
This may be alien technology,
but dividing by zero is still an error!
Expected response: DIV0_ERR

* Syntax Error
Invalid expressions due syntax errors.
ex. 3 +* 4 = ?
Expected response: SYNTAX_ERR

* Memory Error
The remote machine is blazingly fast,
but its architecture cannot represent any result
outside the range -1337.00 <= RESULT <= 1337.00
Expected response: MEM_ERR
'''

def solve(problem):
	try:
		ans = float(eval(problem))
	except ZeroDivisionError:
		return b'DIV0_ERR'
	except SyntaxError:
		return b'SYNTAX_ERR'

	if not (-1337.00 <= ans <= 1337.00):
		return b'MEM_ERR'
	else:
		return str(round(ans, 2))



p = remote('142.93.38.14', 31284)

p.sendlineafter('> ','1')

p.recvline()
p.recvline()
p.recvline()

for _ in range(500):
	output = p.recvline()
	print(output)
	prob = output.decode().strip().split(' =')[0].split(': ')[1]
	print(prob)
	ans = solve(prob)
	print(ans)
	p.sendlineafter('> ',ans)

flag = p.recvline()
if b"HTB{" in flag:
	print(flag.decode())

p.interactive()
