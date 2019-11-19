from mine.collections import Queue

class A:
	def __del__(self):
		print("deleted")

if __name__ == '__main__':
	q = Queue()
	q.enqueue(A())
	q.dequeue()
	input()