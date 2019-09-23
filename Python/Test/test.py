from measurer import m
from time import sleep

@m
def a():
	sleep(0.5)
	print("1 done")

@m(output=lambda x: print(round(x, 4)))
def b():
	sleep(0.5)
	print("2")

a()
b()