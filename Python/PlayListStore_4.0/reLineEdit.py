from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class reLineEdit(QLineEdit):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)