# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/SearchTitleForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_search_form(object):
    def setupUi(self, search_form):
        search_form.setObjectName("search_form")
        search_form.resize(402, 286)
        search_form.setMinimumSize(QtCore.QSize(402, 286))
        self.verticalLayout = QtWidgets.QVBoxLayout(search_form)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.search_edit = QtWidgets.QLineEdit(search_form)
        self.search_edit.setMinimumSize(QtCore.QSize(25, 0))
        self.search_edit.setMaxLength(80)
        self.search_edit.setObjectName("search_edit")
        self.verticalLayout.addWidget(self.search_edit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.found = QtWidgets.QLabel(search_form)
        self.found.setObjectName("found")
        self.horizontalLayout.addWidget(self.found)
        self.genre_search = QtWidgets.QCheckBox(search_form)
        self.genre_search.setObjectName("genre_search")
        self.horizontalLayout.addWidget(self.genre_search, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.result = QtWidgets.QTableWidget(search_form)
        self.result.setMinimumSize(QtCore.QSize(368, 200))
        self.result.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.result.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.result.setProperty("showDropIndicator", False)
        self.result.setDragDropOverwriteMode(False)
        self.result.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.result.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.result.setTextElideMode(QtCore.Qt.ElideRight)
        self.result.setShowGrid(False)
        self.result.setGridStyle(QtCore.Qt.SolidLine)
        self.result.setCornerButtonEnabled(True)
        self.result.setObjectName("result")
        self.result.setColumnCount(3)
        self.result.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.result.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.result.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.result.setHorizontalHeaderItem(2, item)
        self.result.horizontalHeader().setCascadingSectionResizes(False)
        self.result.horizontalHeader().setDefaultSectionSize(102)
        self.result.horizontalHeader().setHighlightSections(True)
        self.result.horizontalHeader().setMinimumSectionSize(60)
        self.result.horizontalHeader().setSortIndicatorShown(False)
        self.result.horizontalHeader().setStretchLastSection(False)
        self.result.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.result)

        self.retranslateUi(search_form)
        QtCore.QMetaObject.connectSlotsByName(search_form)

    def retranslateUi(self, search_form):
        _translate = QtCore.QCoreApplication.translate
        search_form.setWindowTitle(_translate("search_form", "Найти тайтл"))
        self.search_edit.setPlaceholderText(_translate("search_form", "Название тайтла"))
        self.found.setText(_translate("search_form", "Найдено:0"))
        self.genre_search.setText(_translate("search_form", "Искать по жанру"))
        self.result.setSortingEnabled(False)
        item = self.result.horizontalHeaderItem(0)
        item.setText(_translate("search_form", "Кол-во"))
        item = self.result.horizontalHeaderItem(1)
        item.setText(_translate("search_form", "Название тайтла"))
        item = self.result.horizontalHeaderItem(2)
        item.setText(_translate("search_form", "Плейлист"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    search_form = QtWidgets.QWidget()
    ui = Ui_search_form()
    ui.setupUi(search_form)
    search_form.show()
    sys.exit(app.exec_())
