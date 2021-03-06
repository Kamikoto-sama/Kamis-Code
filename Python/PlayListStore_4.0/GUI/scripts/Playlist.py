# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/Playlist.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Playlist(object):
    def setupUi(self, Playlist):
        Playlist.setObjectName("Playlist")
        Playlist.resize(853, 518)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Playlist)
        self.verticalLayout_2.setContentsMargins(-1, -1, 21, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.topBar = QtWidgets.QFrame(Playlist)
        self.topBar.setMinimumSize(QtCore.QSize(0, 40))
        self.topBar.setMaximumSize(QtCore.QSize(16777215, 45))
        self.topBar.setStyleSheet("")
        self.topBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topBar.setObjectName("topBar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.topBar)
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_frame = QtWidgets.QFrame(self.topBar)
        self.left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_frame.setObjectName("left_frame")
        self.search_edit = QtWidgets.QLineEdit(self.left_frame)
        self.search_edit.setGeometry(QtCore.QRect(70, 7, 182, 25))
        self.search_edit.setMaximumSize(QtCore.QSize(300, 27))
        self.search_edit.setMaxLength(80)
        self.search_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.search_edit.setObjectName("search_edit")
        self.add_title_btn = QtWidgets.QPushButton(self.left_frame)
        self.add_title_btn.setGeometry(QtCore.QRect(0, 7, 70, 25))
        self.add_title_btn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.add_title_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_title_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.add_title_btn.setObjectName("add_title_btn")
        self.search = QtWidgets.QPushButton(self.left_frame)
        self.search.setGeometry(QtCore.QRect(0, 7, 70, 25))
        self.search.setMaximumSize(QtCore.QSize(100, 16777215))
        self.search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search.setFocusPolicy(QtCore.Qt.NoFocus)
        self.search.setObjectName("search")
        self.paste_btn = QtWidgets.QPushButton(self.left_frame)
        self.paste_btn.setEnabled(True)
        self.paste_btn.setGeometry(QtCore.QRect(74, 7, 81, 25))
        self.paste_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.paste_btn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.paste_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.paste_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.paste_btn.setObjectName("paste_btn")
        self.cancel_moving = QtWidgets.QToolButton(self.left_frame)
        self.cancel_moving.setGeometry(QtCore.QRect(154, 7, 25, 25))
        self.cancel_moving.setMinimumSize(QtCore.QSize(0, 0))
        self.cancel_moving.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_moving.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cancel_moving.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\../Icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancel_moving.setIcon(icon)
        self.cancel_moving.setIconSize(QtCore.QSize(25, 25))
        self.cancel_moving.setObjectName("cancel_moving")
        self.search.raise_()
        self.search_edit.raise_()
        self.add_title_btn.raise_()
        self.paste_btn.raise_()
        self.cancel_moving.raise_()
        self.horizontalLayout.addWidget(self.left_frame)
        self.row_count = QtWidgets.QLabel(self.topBar)
        self.row_count.setObjectName("row_count")
        self.horizontalLayout.addWidget(self.row_count)
        self.frame_2 = QtWidgets.QFrame(self.topBar)
        self.frame_2.setObjectName("frame_2")
        self.del_pl = QtWidgets.QPushButton(self.frame_2)
        self.del_pl.setGeometry(QtCore.QRect(205, 6, 80, 25))
        self.del_pl.setMaximumSize(QtCore.QSize(100, 16777215))
        self.del_pl.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.del_pl.setFocusPolicy(QtCore.Qt.NoFocus)
        self.del_pl.setObjectName("del_pl")
        self.rename = QtWidgets.QPushButton(self.frame_2)
        self.rename.setGeometry(QtCore.QRect(82, 6, 121, 25))
        self.rename.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.rename.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.rename.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rename.setObjectName("rename")
        self.horizontalLayout.addWidget(self.frame_2)
        self.verticalLayout_2.addWidget(self.topBar)
        self.scrollArea = QtWidgets.QScrollArea(Playlist)
        self.scrollArea.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.widget = QtWidgets.QWidget()
        self.widget.setGeometry(QtCore.QRect(0, 0, 821, 461))
        self.widget.setObjectName("widget")
        self.row_list = QtWidgets.QVBoxLayout(self.widget)
        self.row_list.setContentsMargins(5, 5, 5, 5)
        self.row_list.setSpacing(5)
        self.row_list.setObjectName("row_list")
        self.scrollArea.setWidget(self.widget)
        self.verticalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(Playlist)
        QtCore.QMetaObject.connectSlotsByName(Playlist)

    def retranslateUi(self, Playlist):
        _translate = QtCore.QCoreApplication.translate
        Playlist.setWindowTitle(_translate("Playlist", "Form"))
        self.search_edit.setPlaceholderText(_translate("Playlist", "Название тайтла"))
        self.add_title_btn.setText(_translate("Playlist", "Добавить"))
        self.search.setText(_translate("Playlist", "Искать"))
        self.paste_btn.setToolTip(_translate("Playlist", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Вставить тайтл в этот плейлист</span></p></body></html>"))
        self.paste_btn.setText(_translate("Playlist", "Вставить"))
        self.cancel_moving.setToolTip(_translate("Playlist", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Отменить перемещение</span></p></body></html>"))
        self.row_count.setText(_translate("Playlist", "Тайтлов в плейлисте:0"))
        self.del_pl.setToolTip(_translate("Playlist", "Удалить выбранный плейлист"))
        self.del_pl.setText(_translate("Playlist", "Удалить"))
        self.rename.setText(_translate("Playlist", "Переименовать"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Playlist = QtWidgets.QWidget()
    ui = Ui_Playlist()
    ui.setupUi(Playlist)
    Playlist.show()
    sys.exit(app.exec_())
