# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets,QtCore
import P

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

app = QtWidgets.QApplication(sys.argv)   
exe = Main()
exe.show()
sys.exit(app.exec_())