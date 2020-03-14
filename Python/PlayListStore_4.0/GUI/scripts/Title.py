# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/Title.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(813, 34)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setAutoFillBackground(True)
        Form.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.t_row = QtWidgets.QFrame(Form)
        self.t_row.setEnabled(True)
        self.t_row.setMinimumSize(QtCore.QSize(0, 0))
        self.t_row.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.t_row.setFrameShadow(QtWidgets.QFrame.Raised)
        self.t_row.setObjectName("t_row")
        self.row_layout = QtWidgets.QVBoxLayout(self.t_row)
        self.row_layout.setContentsMargins(0, 0, 0, 0)
        self.row_layout.setSpacing(5)
        self.row_layout.setObjectName("row_layout")
        self.hor_layout = QtWidgets.QHBoxLayout()
        self.hor_layout.setSpacing(0)
        self.hor_layout.setObjectName("hor_layout")
        self.con_date = ExLineEdit(self.t_row)
        self.con_date.setMinimumSize(QtCore.QSize(0, 30))
        self.con_date.setMaximumSize(QtCore.QSize(150, 16777215))
        self.con_date.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.con_date.setFocusPolicy(QtCore.Qt.NoFocus)
        self.con_date.setMaxLength(10)
        self.con_date.setAlignment(QtCore.Qt.AlignCenter)
        self.con_date.setReadOnly(True)
        self.con_date.setObjectName("con_date")
        self.hor_layout.addWidget(self.con_date)
        self.status = QtWidgets.QLabel(self.t_row)
        self.status.setMinimumSize(QtCore.QSize(30, 30))
        self.status.setText("")
        self.status.setObjectName("status")
        self.hor_layout.addWidget(self.status)
        self.count = ExLineEdit(self.t_row)
        self.count.setMinimumSize(QtCore.QSize(0, 30))
        self.count.setMaximumSize(QtCore.QSize(100, 16777215))
        self.count.setFocusPolicy(QtCore.Qt.NoFocus)
        self.count.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.count.setMaxLength(4)
        self.count.setAlignment(QtCore.Qt.AlignCenter)
        self.count.setReadOnly(True)
        self.count.setObjectName("count")
        self.hor_layout.addWidget(self.count)
        self.title_name = ExLineEdit(self.t_row)
        self.title_name.setEnabled(True)
        self.title_name.setMinimumSize(QtCore.QSize(0, 30))
        self.title_name.setFocusPolicy(QtCore.Qt.NoFocus)
        self.title_name.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.title_name.setText("")
        self.title_name.setMaxLength(80)
        self.title_name.setDragEnabled(False)
        self.title_name.setReadOnly(True)
        self.title_name.setObjectName("title_name")
        self.hor_layout.addWidget(self.title_name)
        self.row_layout.addLayout(self.hor_layout)
        self.verticalLayout.addWidget(self.t_row)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.con_date.setPlaceholderText(_translate("Form", "Дата"))
        self.count.setPlaceholderText(_translate("Form", "Серии"))
        self.title_name.setPlaceholderText(_translate("Form", "Название тайтла"))
from gui.exobjects import ExLineEdit


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
