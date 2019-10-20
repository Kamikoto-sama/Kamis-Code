class D(dict):
	def __getitem__(self, key):
		value = super().__getitem__(key)
		return value() if callable(value) else value

