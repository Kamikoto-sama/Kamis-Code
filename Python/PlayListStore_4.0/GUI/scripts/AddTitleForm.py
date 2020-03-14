# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/AddTitleForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(360, 257)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.add_form = QtWidgets.QFrame(Form)
        self.add_form.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.add_form.setFrameShadow(QtWidgets.QFrame.Raised)
        self.add_form.setObjectName("add_form")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.add_form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title_name = QtWidgets.QLineEdit(self.add_form)
        self.title_name.setMaxLength(80)
        self.title_name.setAlignment(QtCore.Qt.AlignCenter)
        self.title_name.setObjectName("title_name")
        self.horizontalLayout.addWidget(self.title_name)
        self.count = QtWidgets.QLineEdit(self.add_form)
        self.count.setMaximumSize(QtCore.QSize(50, 16777215))
        self.count.setMaxLength(4)
        self.count.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.count.setAlignment(QtCore.Qt.AlignCenter)
        self.count.setObjectName("count")
        self.horizontalLayout.addWidget(self.count)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.is_con = QtWidgets.QCheckBox(self.add_form)
        self.is_con.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.is_con.setFocusPolicy(QtCore.Qt.NoFocus)
        self.is_con.setObjectName("is_con")
        self.horizontalLayout_5.addWidget(self.is_con)
        self.is_finished = QtWidgets.QCheckBox(self.add_form)
        self.is_finished.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.is_finished.setFocusPolicy(QtCore.Qt.NoFocus)
        self.is_finished.setObjectName("is_finished")
        self.horizontalLayout_5.addWidget(self.is_finished)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.genre = QtWidgets.QLineEdit(self.add_form)
        self.genre.setMaxLength(60)
        self.genre.setObjectName("genre")
        self.verticalLayout.addWidget(self.genre)
        self.link = QtWidgets.QLineEdit(self.add_form)
        self.link.setMaxLength(2000)
        self.link.setObjectName("link")
        self.verticalLayout.addWidget(self.link)
        self.desc = QtWidgets.QTextEdit(self.add_form)
        self.desc.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.desc.setTabChangesFocus(True)
        self.desc.setAcceptRichText(False)
        self.desc.setObjectName("desc")
        self.verticalLayout.addWidget(self.desc)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.ok = QtWidgets.QPushButton(self.add_form)
        self.ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ok.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ok.setObjectName("ok")
        self.horizontalLayout_6.addWidget(self.ok)
        self.cancel = QtWidgets.QPushButton(self.add_form)
        self.cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout_6.addWidget(self.cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.gridLayout.addWidget(self.add_form, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.title_name.setPlaceholderText(_translate("Form", "Название тайтла"))
        self.count.setToolTip(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Количество серий</span></p></body></html>"))
        self.count.setText(_translate("Form", "12"))
        self.count.setPlaceholderText(_translate("Form", "Кол-во"))
        self.is_con.setText(_translate("Form", "Это продолжение"))
        self.is_finished.setText(_translate("Form", "Тайтл не закончен"))
        self.genre.setPlaceholderText(_translate("Form", "Жанр"))
        self.link.setPlaceholderText(_translate("Form", "Ссылка"))
        self.desc.setPlaceholderText(_translate("Form", "Описание"))
        self.ok.setText(_translate("Form", "OK"))
        self.cancel.setText(_translate("Form", "Отмена"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
