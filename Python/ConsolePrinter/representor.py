class Representor:
	def __init__(self, string):
		self.string = string
		
	def __repr__(self):
		return self.string
	
	def representString(self, string = None):
		self.string = string if string is not None else self.string
		return self