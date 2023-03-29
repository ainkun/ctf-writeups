#python3 -c "print('A'*49968);print('A'*32)" | nc mercury.picoctf.net 41934

enc_A = 0x2366101d3922231d3979201d3923751d3971751d3927791d3971713a1d392525

plain_A = 0x4141414141414141414141414141414141414141414141414141414141414141

enc_flag = 0x0345376e1e5406691d5c076c4050046e4000036a1a005c6b1904531d3941055d

plain_flag = ''

key = ''

# Thats What the program does:
# enc_flag = key ^ plain_flag

# We used all remaining key to encrypt junk, then use As to encrypt using with the same key values
# enc_A = key ^ plain_A

# To find key we can xor enc_A with the result with the plain A values:
key = enc_A ^ plain_A

# Using the key value to decrypt the flag:
plain_flag = key ^ enc_flag

hex_flag = hex(plain_flag)[2:]

flag = bytes.fromhex(str(hex_flag)).decode()


print("picoCTF{"+str(flag)+"}")
