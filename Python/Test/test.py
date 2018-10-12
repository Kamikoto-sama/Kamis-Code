import PyQt5

def array(a:list):
	a[0] = 5

def Main():
	n = 1
	a = [0,1,2]
	array(a)
	print(a)