p = 0xdd6cc28d
g = 0x83e21c05
A = 0xcfabb6dd
B = 0xc4a21ba9

R = IntegerModRing(p)

#A = g^a %p
#B = g^b %p

a = discrete_log(R(A),R(g))
b = discrete_log(R(B),R(g))

print(f"Private Key a: {a}")
print(f"Private Key b: {b}")


C = pow(A, b, p)
assert C == pow(B, a, p)

print(f"Shared Secret: {C}")
