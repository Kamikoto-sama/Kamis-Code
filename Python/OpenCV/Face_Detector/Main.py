# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets,QtCore,QtGui
import Form
import FaceDetect
import os

class Main(QtWidgets.QMainWindow,Form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.select.clicked.connect(self.SelectImage)

    def SelectImage(self):
    	try:
    		image = QtWidgets.QFileDialog.getOpenFileName(self,"Select image",'')[0]
    		FaceDetect.Detect_Faces(image)
    		image = QtGui.QPixmap("image.png")
    		self.label.setPixmap(image)
    		os.remove("image.png")
    	except Exception as e:print(e)

app = QtWidgets.QApplication(sys.argv)   
exe = Main()
exe.show()
sys.exit(app.exec_())