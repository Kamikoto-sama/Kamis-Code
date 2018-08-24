# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI\\Main_Form.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setStyleSheet("#frame,#sideBar{\n"
"background-color:silver;\n"
"}\n"
"#list{\n"
"height: auto;\n"
"}\n"
"#titleName,#count{\n"
"font: 75 12pt \"Consolas\";\n"
"}\n"
"QWidget{\n"
"font-family:\"Consolas\";\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(0, 45))
        self.widget.setObjectName("widget")
        self.addP = QtWidgets.QPushButton(self.widget)
        self.addP.setGeometry(QtCore.QRect(700, 10, 75, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.addP.setFont(font)
        self.addP.setObjectName("addP")
        self.delP = QtWidgets.QPushButton(self.widget)
        self.delP.setGeometry(QtCore.QRect(90, 10, 75, 23))
        self.delP.setObjectName("delP")
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setGeometry(QtCore.QRect(350, 10, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.adv = QtWidgets.QPushButton(self.widget)
        self.adv.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.adv.setObjectName("adv")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(512, 10, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self._adv = QtWidgets.QPushButton(self.widget)
        self._adv.setGeometry(QtCore.QRect(170, 10, 75, 23))
        self._adv.setObjectName("_adv")
        self.verticalLayout.addWidget(self.widget)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addP.setToolTip(_translate("MainWindow", "<html><head/><body><p>Create playlist</p></body></html>"))
        self.addP.setText(_translate("MainWindow", "ADD"))
        self.delP.setText(_translate("MainWindow", "DEL"))
        self.adv.setText(_translate("MainWindow", "CLEAR"))
        self.lineEdit.setToolTip(_translate("MainWindow", "Tool"))
        self.lineEdit.setStatusTip(_translate("MainWindow", "Alo"))
        self.lineEdit.setWhatsThis(_translate("MainWindow", "Aloha"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Playlist name"))
        self._adv.setText(_translate("MainWindow", "ADV2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

