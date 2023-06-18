import hlextend

message = b'I guess you are just gonna have to include this!'
KEYLEN = 64

org = 'c054bccebbfee707011b64ea255e438b33d7e2cd' #To be generated after sending the above message to oracle 

new_message = b'test'

import hlextend
sha = hlextend.new('sha1')
_val = sha.extend(b'text', message, KEYLEN, org) # https://github.com/stephenbradshaw/hlextend
print(f'msg(hex): {bytes.hex(_val)}')
print(f'tag(hex): {sha.hexdigest()}')

#flag{4179e0a0f6ddc273a8a18440c979bbb7}

#https://www.synopsys.com/blogs/software-security/forging-sha-1-mac-using-length-extension-attack-python/
#https://www.youtube.com/watch?v=6QQ4kgDWQ9w