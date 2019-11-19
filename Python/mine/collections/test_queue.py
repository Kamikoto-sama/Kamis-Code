from .queue import Queue
from .exceptions import *
from unittest import TestCase

class Queue_Should(TestCase):
	def test_increasesCount_whenEnqueueItems(self):
		queue = Queue()
		queue.enqueue(1)
		assert queue.count == 1
	
	def test_containsItems_whenInitedWithIterable(self):
		queue = Queue([1,2,3])
		assert queue.count == 3
		assert list(queue) == [1,2,3]
		
	def test_first_raisesException_whenQueueIsEmpty(self):
		queue = Queue()
		self.assertRaises(WrongOperationError, lambda: queue.first)

	def test_last_raisesException_whenQueueIsEmpty(self):
		queue = Queue()
		self.assertRaises(WrongOperationError, lambda: queue.last)
		
	def test_dequeueExtraItem_whenMaxItemSet(self):
		queue = Queue(2)
		for i in range(5):
			queue.enqueue(i)
		assert queue.count == 2
		
	def test_dequeue_raisesException_whenQueueEmpty(self):
		queue = Queue()
		self.assertRaises(WrongOperationError, lambda: queue.dequeue())
		
	def test_dequeue_returnsFirstAddedItem(self):
		queue = Queue()
		for i in range(5):
			queue.enqueue(i)
		assert queue.dequeue() == 0
		
	def test_removesObjectReferences_AfterDequeue(self):
		objRemoved = False
		class Obj:
			def __del__(self):
				globals()['objRemoved'] = True
		
		queue = Queue()
		queue.enqueue(Obj())
		queue.dequeue()
		assert objRemoved