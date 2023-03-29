import random
import os

alphabet = list('abcdefghijklmnopqrstuvwxyz')
shuffled = list('SPRFWHKJOQZLDCUVYEMNBTIAGX')
dictionary = dict(zip(alphabet, shuffled))


flag = open('flag.txt', 'r').read()

decrypted = ''.join([dictionary[c] if c in dictionary else c for c in flag])
print(decrypted.lower())