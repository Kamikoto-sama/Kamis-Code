# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI\\New_Playlist.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewTab(object):
    def setupUi(self, NewTab):
        NewTab.setObjectName("NewTab")
        NewTab.resize(807, 518)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(NewTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(NewTab)
        self.frame.setMinimumSize(QtCore.QSize(0, 39))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 45))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.addT = QtWidgets.QPushButton(self.frame)
        self.addT.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.addT.setObjectName("addT")
        self.setTName = QtWidgets.QLineEdit(self.frame)
        self.setTName.setEnabled(True)
        self.setTName.setGeometry(QtCore.QRect(90, 10, 231, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.setTName.setFont(font)
        self.setTName.setInputMask("")
        self.setTName.setText("")
        self.setTName.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.setTName.setAlignment(QtCore.Qt.AlignCenter)
        self.setTName.setClearButtonEnabled(False)
        self.setTName.setObjectName("setTName")
        self.verticalLayout_2.addWidget(self.frame)
        self.titleList = QtWidgets.QTableWidget(NewTab)
        self.titleList.setObjectName("titleList")
        self.titleList.setColumnCount(0)
        self.titleList.setRowCount(0)
        self.verticalLayout_2.addWidget(self.titleList)

        self.retranslateUi(NewTab)
        QtCore.QMetaObject.connectSlotsByName(NewTab)

    def retranslateUi(self, NewTab):
        _translate = QtCore.QCoreApplication.translate
        NewTab.setWindowTitle(_translate("NewTab", "Form"))
        self.addT.setText(_translate("NewTab", "AddT"))
        self.setTName.setToolTip(_translate("NewTab", "Tool"))
        self.setTName.setStatusTip(_translate("NewTab", "Alo"))
        self.setTName.setWhatsThis(_translate("NewTab", "Aloha"))
        self.setTName.setPlaceholderText(_translate("NewTab", "Title name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewTab = QtWidgets.QWidget()
    ui = Ui_NewTab()
    ui.setupUi(NewTab)
    NewTab.show()
    sys.exit(app.exec_())

