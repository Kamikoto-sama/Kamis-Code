def overloaded(method):
	return OverloadedMethod(method)

class OverloadedMethod:
	def __init__(self, method):
		self.name = method.__name__
		self.overloadCount = 0

	def __call__(self, *args, **kwargs):
		pass

	def overload(self, method):
		pass

	def annotationEquals():
		pass