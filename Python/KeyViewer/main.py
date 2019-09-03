from sys import argv
from PyQt5.uic import loadUi
from PyQt5.QtGui import QMouseEvent
from keyListener import KeyListener
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QPropertyAnimation
from exCollections import Queue
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem

StylesFile = "style.css"
PositionsFile = "pos.ini"
AnimDuration = 200

def loadStyle() -> str:
	with open(StylesFile) as style:
		return style.read()


def loadPosition() -> QPoint:
	with open(PositionsFile) as pos:
		return QPoint(*(int(p) for p in pos.readline().split()))


class Main(QWidget):
	def __init__(self):
		try:
			flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.SubWindow
			super(Main, self).__init__(None, flags)
			loadUi("ui/Main.ui", self)
			self.setStyleSheet(loadStyle())

			# self.setAttribute(Qt.WA_TranslucentBackground, True)
			self.oldPos = loadPosition()
			self.move(self.oldPos)
			self.show()

			self.keyListener = None
			self.restartListening()

			self.queue = [self.label1, self.label2, self.label3]
			self.new: QLabel = self.label3
			self.lastKey = None
		except Exception as e:
			print(e)

	def restartListening(self):
		if self.keyListener is not None:
			self.keyListener.stop()
		self.keyListener = KeyListener(self.updateDisplay)
		self.keyListener.listen()

	def updateDisplay(self, text):
		self.new: QLabel = self.queue[2]
		self.new.setText(text)
		self.new.hide()
		self.moveFrames()
		
	def moveFrames(self):
		xPos = self.geometry().width()
		lastAnim = QPropertyAnimation(self.new, b"pos")
		lastAnim.setStartValue(QPoint(xPos, 140))
		lastAnim.setEndValue(QPoint(0, 140))
		lastAnim.setDuration(AnimDuration)
		lastAnim.finished.connect(self.new.show)
		
		firstAnim = QPropertyAnimation(self.queue[1], b"y")
		firstAnim.setEndValue(0)
		firstAnim.setDuration(AnimDuration)
		
		secondAnim = QPropertyAnimation(self.queue[2], b"x")
		secondAnim.setEndValue(70)
		secondAnim.setDuration(AnimDuration)
		secondAnim.finished.connect(lastAnim.start)
		
		firstAnim.start()
		secondAnim.start()
		self.queue.insert(0, self.queue.pop(2))

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event: QMouseEvent):
		delta = QPoint(event.globalPos() - self.oldPos)
		self.move(self.x() + delta.x(), self.y() + delta.y())
		self.oldPos = event.globalPos()

	def mouseReleaseEvent(self, event: QMouseEvent):
		event.accept()
		pos = self.geometry().topLeft()
		with open(PositionsFile, "w") as file:
			file.write("%s %s" % (pos.x(), pos.y()))

	def mouseDoubleClickEvent(self, event: QMouseEvent):
		# Settings(self).show()
		self.close()

	def closeEvent(self, event):
		try:
			self.keyListener.stop()
			event.accept()
			print("Press any key to exit...")
		except Exception as e:
			print(e)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()


class Settings(QWidget):
	def __init__(self, parent):
		try:
			super(Settings, self).__init__(parent, Qt.Window | Qt.WindowCloseButtonHint)
			loadUi("ui/Settings.ui", self)

			self.exitBtn.clicked.connect(self.exit)
		except Exception as e:
			print(e)

	def exit(self):
		try:
			self.close()
			self.parent().close()
		except Exception as e:
			print(e)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()


if __name__ == '__main__':
	app = QApplication(argv)
	main = Main()
	app.exec_()
