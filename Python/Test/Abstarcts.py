def abstract(obj):
	if isinstance(obj, type):
		return AbstractClass(obj)
	elif callable(obj):
		return AbstractMethod(obj)
	raise ArgumentException("Unsupportable type: %s" % type(obj))

class AbstractClass:
	def __new__(cls, *args, **kwargs):
		

class AbstractMethod:
	def __init__(self, function):
		self.name = function.__name__
		self.argsCount = function.__code__.co_argcount
		self.target = function

	def __call__(self, *args, **kwargs):
		return self.target(*args, **kwargs)

class ArgumentException(BaseException):
	pass
