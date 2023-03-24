dictionary = {}
alphabet = list('abcdefghijklmnopqrstuvwxyz')

for character in alphabet:
	dictionary[character] = 0

COUNTER = 0

with open("study-guide.txt", "r") as f:
	for word in f:
		for charac in word.strip():
			if charac in dictionary:
				dictionary[charac] += 1
				COUNTER +=1

print(f"Letter Counter: {COUNTER}\n")
print(f"Letter Counter dataset: \n{dictionary}\n")

frequency = {}

for character in dictionary:
	frequency[character] = round((dictionary[character]/COUNTER)*100,3)

print(f"Letter frequency: \n{frequency}")


'''
Letter Counter: 2905856

Letter Counter dataset: 
{'a': 206355, 'b': 96529, 'c': 205401, 'd': 66435, 'e': 14940, 'f': 76513, 'g': 17173, 'h': 3251, 'i': 214772, 'j': 4794, 'k': 11862, 'l': 162351, 'm': 90628, 'n': 131465, 'o': 107082, 'p': 27458, 'q': 57699, 'r': 311363, 's': 87009, 't': 216936, 'u': 49432, 'v': 198197, 'w': 270080, 'x': 239284, 'y': 30493, 'z': 8354}

Letter frequency: 
{'a': 7.101, 'b': 3.322, 'c': 7.069, 'd': 2.286, 'e': 0.514, 'f': 2.633, 'g': 0.591, 'h': 0.112, 'i': 7.391, 'j': 0.165, 'k': 0.408, 'l': 5.587, 'm': 3.119, 'n': 4.524, 'o': 3.685, 'p': 0.945, 'q': 1.986, 'r': 10.715, 's': 2.994, 't': 7.465, 'u': 1.701, 'v': 6.821, 'w': 9.294, 'x': 8.235, 'y': 1.049, 'z': 0.287}

'''