# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI\\New_Title.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(790, 32)
        Form.setMaximumSize(QtCore.QSize(16777215, 32))
        Form.setAutoFillBackground(True)
        Form.setStyleSheet("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.titleName = QtWidgets.QLineEdit(Form)
        self.titleName.setMinimumSize(QtCore.QSize(0, 30))
        self.titleName.setText("")
        self.titleName.setObjectName("titleName")
        self.horizontalLayout.addWidget(self.titleName)
        self.count = QtWidgets.QLineEdit(Form)
        self.count.setMinimumSize(QtCore.QSize(0, 30))
        self.count.setMaximumSize(QtCore.QSize(100, 16777215))
        self.count.setObjectName("count")
        self.horizontalLayout.addWidget(self.count)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

