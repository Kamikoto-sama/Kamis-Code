from keyboard import read_hotkey
from threading import Thread

ControlKeys = {hash("ctrl"), hash("alt"), hash("shift")}

class KeyListener(Thread):
	def __init__(self, output, exitKey=None):
		super().__init__()
		self.output = output
		self.exitKey = hash(exitKey)
		self.listen = self.start
		self.__alive = True

	def run(self):
		while self.__alive:
			shortcut = read_hotkey(False)
			if hash(shortcut) == self.exitKey:
				return
			keys = shortcut.split("+")
			if len(keys) > 1 and self.validateKeys(keys):
				self.output(shortcut)

	def stop(self):
		self.__alive = False

	@staticmethod
	def validateKeys(keys):
		hasCKey = False
		hasOtherKey = False
		for key in keys:
			if hash(key) in ControlKeys:
				hasCKey = True
			else:
				hasOtherKey = True
		return hasCKey and hasOtherKey
	
if __name__ == '__main__':
	KeyListener(print, "shift+Q").listen()