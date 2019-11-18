from .node import Node
from .exceptions import WrongOperationError, ArgumentException

class Queue:
	def __init__(self, iterable=None, maxCount=-1):
		if iterable is not None and not hasattr(iterable, "__iter__"):
			raise ArgumentException("iterable must implement __iter__ method")
		
		self.__count = 0
		self.__head = None
		self.__tail = None
		self.__maxCount = iterable if iterable is int else maxCount
		self.fill(iterable)

	def fill(self, items):
		if items is None:
			return
		for item in items:
			self.enqueue(item)
		
	@property
	def maxCount(self):
		return self.__maxCount

	@property
	def count(self):
		return self.__count

	@property
	def first(self):
		return self.__head.value

	@property
	def last(self):
		return self.__tail.value

	def enqueue(self, value):
		newNode = Node(value)
		if self.__tail is None:
			self.__head = newNode
		else:
			self.__tail.next = newNode
		self.__tail = newNode
		if self.count == self.maxCount:
			self.dequeue()
		self.__count += 1

	def dequeue(self):
		if self.count == 0:
			raise WrongOperationError("Queue is empty")
		value = self.first
		self.__head = self.__head.next
		self.__count -= 1
		return value

	def clear(self):
		self.__head = None
		self.__tail = None
		self.__count = 0

	def __contains__(self, item):
		for node in self:
			if node == item:
				return True
		return False

	def __iter__(self):
		current = self.__head
		while current is not None:
			yield current.value
			current = current.next

	def __len__(self):
		return self.__count

	def __repr__(self):
		return "(" + " < ".join(map(str, self)) + ")"