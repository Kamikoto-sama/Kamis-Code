from typing import Dict

class PatternReader:
	def __init__(self, fileName):
		self.fileName = fileName
		
	def readPattern(self) -> Dict[int, str]:
		with open(self.fileName, 'r') as file:
			patternLines = file.readlines()
			for line in patternLines:
				