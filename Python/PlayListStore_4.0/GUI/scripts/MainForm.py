# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/MainForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 620)
        MainWindow.setMinimumSize(QtCore.QSize(900, 345))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\../icons/pls.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        MainWindow.setIconSize(QtCore.QSize(64, 64))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_bar = QtWidgets.QFrame(self.centralwidget)
        self.main_bar.setMinimumSize(QtCore.QSize(0, 50))
        self.main_bar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.main_bar.setObjectName("main_bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.main_bar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.main_bar)
        self.frame_2.setMaximumSize(QtCore.QSize(300, 32))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.options = QtWidgets.QPushButton(self.frame_2)
        self.options.setGeometry(QtCore.QRect(10, 0, 74, 30))
        self.options.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.options.setFocusPolicy(QtCore.Qt.NoFocus)
        self.options.setObjectName("options")
        self.con_info = QtWidgets.QToolButton(self.frame_2)
        self.con_info.setGeometry(QtCore.QRect(87, 0, 32, 30))
        self.con_info.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.con_info.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".\\../Icons/сon_info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.con_info.setIcon(icon1)
        self.con_info.setIconSize(QtCore.QSize(32, 32))
        self.con_info.setObjectName("con_info")
        self.horizontalLayout.addWidget(self.frame_2)
        self.pl_list = QtWidgets.QComboBox(self.main_bar)
        self.pl_list.setMinimumSize(QtCore.QSize(100, 0))
        self.pl_list.setMaximumSize(QtCore.QSize(240, 30))
        self.pl_list.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pl_list.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pl_list.setEditable(False)
        self.pl_list.setMaxVisibleItems(6)
        self.pl_list.setObjectName("pl_list")
        self.horizontalLayout.addWidget(self.pl_list)
        self.frame = QtWidgets.QFrame(self.main_bar)
        self.frame.setMinimumSize(QtCore.QSize(0, 50))
        self.frame.setMaximumSize(QtCore.QSize(323, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.add_pl = QtWidgets.QToolButton(self.frame)
        self.add_pl.setGeometry(QtCore.QRect(290, 10, 32, 32))
        self.add_pl.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_pl.setFocusPolicy(QtCore.Qt.NoFocus)
        self.add_pl.setStatusTip("")
        self.add_pl.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(".\\../Icons/addP.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_pl.setIcon(icon2)
        self.add_pl.setIconSize(QtCore.QSize(32, 32))
        self.add_pl.setObjectName("add_pl")
        self.pl_name = QtWidgets.QLineEdit(self.frame)
        self.pl_name.setEnabled(True)
        self.pl_name.setGeometry(QtCore.QRect(34, 11, 255, 30))
        self.pl_name.setInputMask("")
        self.pl_name.setText("")
        self.pl_name.setMaxLength(30)
        self.pl_name.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.pl_name.setAlignment(QtCore.Qt.AlignCenter)
        self.pl_name.setClearButtonEnabled(False)
        self.pl_name.setObjectName("pl_name")
        self.close_pl_name = QtWidgets.QToolButton(self.frame)
        self.close_pl_name.setGeometry(QtCore.QRect(0, 10, 32, 32))
        self.close_pl_name.setMinimumSize(QtCore.QSize(30, 30))
        self.close_pl_name.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close_pl_name.setFocusPolicy(QtCore.Qt.NoFocus)
        self.close_pl_name.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(".\\../Icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close_pl_name.setIcon(icon3)
        self.close_pl_name.setIconSize(QtCore.QSize(28, 28))
        self.close_pl_name.setObjectName("close_pl_name")
        self.viewed_count = QtWidgets.QLabel(self.frame)
        self.viewed_count.setGeometry(QtCore.QRect(4, -1, 253, 50))
        self.viewed_count.setMaximumSize(QtCore.QSize(400, 16777215))
        self.viewed_count.setObjectName("viewed_count")
        self.viewed_count.raise_()
        self.add_pl.raise_()
        self.pl_name.raise_()
        self.close_pl_name.raise_()
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout.addWidget(self.main_bar)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pl_name, self.add_pl)
        MainWindow.setTabOrder(self.add_pl, self.close_pl_name)
        MainWindow.setTabOrder(self.close_pl_name, self.tabWidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PlayListStore 4"))
        self.options.setText(_translate("MainWindow", "Опции"))
        self.con_info.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Имеются продолжения!</span></p></body></html>"))
        self.add_pl.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#000000;white-space: nowrap;\">Создать новый плейлист</span></p></body></html>"))
        self.pl_name.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Введите название плейлиста</span></p></body></html>"))
        self.pl_name.setStatusTip(_translate("MainWindow", "Alo"))
        self.pl_name.setWhatsThis(_translate("MainWindow", "Aloha"))
        self.pl_name.setPlaceholderText(_translate("MainWindow", "Название плейлиста"))
        self.viewed_count.setText(_translate("MainWindow", "Всего просмотрено:0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())