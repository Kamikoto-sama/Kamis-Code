from threading import Thread
from time import sleep


class A(Thread):
	def __init__(self):
		super().__init__()
		
	def run(self):
		sleep(2)
		print("helo")
		
if __name__ == '__main__':
	A().start()
	print(10)