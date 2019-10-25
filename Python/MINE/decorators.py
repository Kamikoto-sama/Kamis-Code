from .exceptions import InheritingError
from .overload import *

def final(cls):
	def init(*args):
		raise InheritingError("Final class can't be inherited")
	setattr(cls, "__init_subclass__", init)
	return cls