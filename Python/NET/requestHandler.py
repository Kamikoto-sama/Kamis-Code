from json import JSONDecoder

class Request:
	def __init__(self, action, obj):
		self.action = action
		self.obj = obj
		
class RequestHandler:
	@staticmethod
	def toRequest(rawRequest):
		requestDict = JSONDecoder().decode(rawRequest)
		return Request(**requestDict)