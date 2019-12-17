from .queue import Queue
from .exceptions import *

def test_containsItems_whenInitedWithIterable():
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