# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/Settings.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(247, 107)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\../icons/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.total_added = QtWidgets.QLabel(Form)
        self.total_added.setAlignment(QtCore.Qt.AlignCenter)
        self.total_added.setObjectName("total_added")
        self.verticalLayout.addWidget(self.total_added)
        self.auto_update = QtWidgets.QCheckBox(Form)
        self.auto_update.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.auto_update.setFocusPolicy(QtCore.Qt.NoFocus)
        self.auto_update.setObjectName("auto_update")
        self.verticalLayout.addWidget(self.auto_update, 0, QtCore.Qt.AlignHCenter)
        self.select_font = QtWidgets.QPushButton(Form)
        self.select_font.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.select_font.setFocusPolicy(QtCore.Qt.NoFocus)
        self.select_font.setObjectName("select_font")
        self.verticalLayout.addWidget(self.select_font)
        self.info = QtWidgets.QPushButton(Form)
        self.info.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.info.setFocusPolicy(QtCore.Qt.NoFocus)
        self.info.setObjectName("info")
        self.verticalLayout.addWidget(self.info)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Settings"))
        self.total_added.setText(_translate("Form", "Всего добавленно тайтлов:000"))
        self.auto_update.setText(_translate("Form", "Включить автообновления"))
        self.select_font.setText(_translate("Form", "Поменять шрифт"))
        self.info.setText(_translate("Form", "Информация"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
