class Contaiter:
	def get(someType):
		if not hasattr(someType):
			return someType()
		annotations = someType.__annotations__
		args = {}
		