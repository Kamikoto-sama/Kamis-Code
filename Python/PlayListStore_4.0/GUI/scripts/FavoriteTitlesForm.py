# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/FavoriteTitlesForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_favorite_form(object):
    def setupUi(self, favorite_form):
        favorite_form.setObjectName("favorite_form")
        favorite_form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(favorite_form)
        self.verticalLayout.setContentsMargins(0, 2, 0, 0)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(2, -1, 2, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.up = QtWidgets.QPushButton(favorite_form)
        self.up.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.up.setFocusPolicy(QtCore.Qt.NoFocus)
        self.up.setObjectName("up")
        self.horizontalLayout.addWidget(self.up)
        self.down = QtWidgets.QPushButton(favorite_form)
        self.down.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.down.setFocusPolicy(QtCore.Qt.NoFocus)
        self.down.setObjectName("down")
        self.horizontalLayout.addWidget(self.down)
        self.del_title = QtWidgets.QPushButton(favorite_form)
        self.del_title.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.del_title.setFocusPolicy(QtCore.Qt.NoFocus)
        self.del_title.setObjectName("del_title")
        self.horizontalLayout.addWidget(self.del_title)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(favorite_form)
        self.table.setMinimumSize(QtCore.QSize(368, 200))
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.table.setProperty("showDropIndicator", False)
        self.table.setDragDropOverwriteMode(False)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setTextElideMode(QtCore.Qt.ElideRight)
        self.table.setShowGrid(False)
        self.table.setGridStyle(QtCore.Qt.SolidLine)
        self.table.setCornerButtonEnabled(True)
        self.table.setObjectName("table")
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setHorizontalHeaderItem(2, item)
        self.table.horizontalHeader().setCascadingSectionResizes(False)
        self.table.horizontalHeader().setDefaultSectionSize(102)
        self.table.horizontalHeader().setHighlightSections(True)
        self.table.horizontalHeader().setMinimumSectionSize(60)
        self.table.horizontalHeader().setSortIndicatorShown(False)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(favorite_form)
        QtCore.QMetaObject.connectSlotsByName(favorite_form)

    def retranslateUi(self, favorite_form):
        _translate = QtCore.QCoreApplication.translate
        favorite_form.setWindowTitle(_translate("favorite_form", "Избранные тайтлы"))
        self.up.setText(_translate("favorite_form", "Вверх"))
        self.down.setText(_translate("favorite_form", "Вниз"))
        self.del_title.setToolTip(_translate("favorite_form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Удалить из избранных</span></p></body></html>"))
        self.del_title.setText(_translate("favorite_form", "Удалить"))
        self.table.setSortingEnabled(False)
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("favorite_form", "Кол-во"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("favorite_form", "Название тайтла"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("favorite_form", "Плейлист"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    favorite_form = QtWidgets.QWidget()
    ui = Ui_favorite_form()
    ui.setupUi(favorite_form)
    favorite_form.show()
    sys.exit(app.exec_())
