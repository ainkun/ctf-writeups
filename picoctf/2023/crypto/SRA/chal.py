from Crypto.Util.number import getPrime, inverse, bytes_to_long
from string import ascii_letters, digits
from random import choice

pt = "".join(choice(ascii_letters + digits) for _ in range(16))
p = getPrime(128)
q = getPrime(128)
n = p * q
e = 65537
d = inverse(e, (p - 1) * (q - 1))

ct = pow(bytes_to_long(pt.encode()), e, n)

print(f"{ct = }")
print(f"{d = }")

print("vainglory?")
vainglory = input("> ").strip()

if vainglory == pt:
    print("Conquered!")
    with open("/challenge/flag.txt") as f:
        print(f.read())
else:
    print("Hubris!")
