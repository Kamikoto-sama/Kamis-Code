from time import time

def m(function=None, output=print):
	def decorator(function):
		def measurerWrap(*args, **kwargs):
			startTime = time()
			functionResult = function(*args, **kwargs)
			output(time() - startTime)
			return functionResult
		return measurerWrap
	return decorator if function is None else decorator(function)