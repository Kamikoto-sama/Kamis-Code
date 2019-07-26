class Queue:
    def __init__(self):
        self.__count = 0
        self.__head: Node = None
        self.__tail: Node = None
        
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
        self.__count += 1
        
    def dequeue(self):
        assert self.count > 0, "Queue is empty"
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

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None
        
class Stack:
    def __init__(self):
        self.__count = 0
        self.__tail: Node = None
        self.__head: Node = None

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
        assert self.count > 0, "Stack is empty"
        value = self.last
        self.__tail = self.__tail.previous
        self.__count -= 1
        return value

    def clear(self):
        self.__tail = None
        self.__head = None
        self.__count = 0

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