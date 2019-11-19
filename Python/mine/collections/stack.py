from .node import Node
from .exceptions import WrongOperationError, ArgumentException

class Stack:
	def __init__(self, iterable=None):
		if iterable is not None and not hasattr(iterable, "__iter__"):
			raise ArgumentException("iterable must implement __iter__ method")
		
		self.__count = 0
		self.__tail = None
		self.__head = None
		if iterable is not None:
			self.fill(iterable)

	def fill(self, items):
		for item in items:
			self.push(item)

	@property
	def count(self):
		return self.__count

	@property
	def first(self):
		return self.__head

	@property
	def last(self):
		return self.__tail.value

	def push(self, value):
		newNode = Node(value)
		newNode.previous = self.__tail
		self.__tail = newNode
		self.__count += 1

	def pop(self):
		if self.count == 0:
			raise WrongOperationError("Stack is empty")
		value = self.last
		self.__tail = self.__tail.previous
		self.__count -= 1
		return value

	def clear(self):
		self.__tail = None
		self.__head = None
		self.__count = 0

	def __len__(self):
		return self.__count

	def __contains__(self, item):
		for node in self:
			if node == item:
				return True
		return False

	def __iter__(self):
		current = self.__tail
		while current is not None:
			yield current.value
			current = current.previous

	def __repr__(self):
		return "(" + " | ".join(map(str, self)) + ")"