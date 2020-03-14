import requests

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
	pool_connections=100,
	pool_maxsize=100)
session.mount('http://', adapter)
while 1:
	req = input(">")
	if req == "q":
		break
	res = session.get('http://localhost:1/test')
	print(res.elapsed, res.content)