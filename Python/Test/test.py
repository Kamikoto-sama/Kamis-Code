from measurer import measurable
from time import sleep

@measurable
def a():
	sleep(0.5)
	print("1 done")

@measurable(output=lambda x: print(round(x, 4)))
def b():
	sleep(0.5)
	print("2")

a()
b()