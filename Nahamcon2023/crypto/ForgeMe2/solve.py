import hlextend
from pwn import *

INJECTION = b'https://www.youtube.com/@_JohnHammond'
KEY = range(10,120)
sha = hlextend.new('sha1')

#nc challenge.nahamcon.com 31345
conn = remote('challenge.nahamcon.com',30978)
conn.recvline() 
message = str(conn.recvuntil("\n\n")).split(":")[-1].strip()[:-5]
print(message)
conn.recvuntil("Choice: ")
conn.sendline(b"1")
conn.recvuntil("msg (hex):")
conn.sendline(bytes.hex(message.encode()))
conn.recvuntil("H(key || msg): ")
org = conn.recvuntil("\n").strip().decode()
print(org)

#KEYLEN = 5
for KEYLEN in KEY:
    print(KEYLEN)
    conn.sendline(b"2")
    _val = sha.extend(INJECTION, message.encode(), KEYLEN, org) 

    conn.recvuntil("msg (hex): ")
    conn.sendline(bytes.hex(_val))
    conn.recvuntil("tag (hex): ")
    conn.sendline(sha.hexdigest())
    res = conn.recvline().strip().decode()
    print(res)
    if res == "True":
        conn.sendline(b"3")
        conn.recvuntil("msg (hex): ")
        conn.sendline(bytes.hex(_val))
        conn.recvuntil("tag (hex): ")
        conn.sendline(sha.hexdigest())
        flag = conn.recvline().decode()
        break

conn.close()
print(flag)