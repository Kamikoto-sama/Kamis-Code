# -*- coding: utf-8 -*-
import os
import sqlite3
import sys

from PyQt5.QtCore import QEventLoop, QTimer, Qt, QPoint, QPropertyAnimation, QEasingCurve, QSize, QRect
from PyQt5.QtGui import QIntValidator, QCursor, QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox, QProxyStyle, QWidget, QHBoxLayout, QPushButton, QMenu, QTabBar, QMainWindow, \
    QApplication, QLineEdit, QStyle, QInputDialog
from PyQt5.uic import loadUi
from time import strftime

# LOAD DB
try:
    if not os.path.exists("Data.pls"):
        db = sqlite3.connect("Data.pls")
        sql = db.cursor()
        sql.execute("CREATE TABLE Playlists (name varchar(100))")
        sql.execute('CREATE TABLE Data (name varchar(10),value varchar(40))')
        sql.execute("""
            CREATE TABLE Titles (
            title_name varchar(255) NOT NULL,
            count int(4),
            id integer PRIMARY KEY AUTOINCREMENT,
            playlist varchar(100),
            icon varchar(15),
            color varchar(15),
            genre varchar(255),
            link text,
            desc text,
            date varchar(10)
            )""")
        sql.execute('INSERT INTO Data VALUES("id","0")')
        sql.execute('INSERT INTO Data VALUES("viewed","0")')
        sql.execute('INSERT INTO Data VALUES("added","0")')
        db.commit()
    else:
        db = sqlite3.connect("Data.pls")
        sql = db.cursor()

    data = [int(d[0]) for d in sql.execute('SELECT value FROM Data')]
    ID = data[0]
    TotalViewed = data[1]
    TotalAdded = data[2]
except Exception as e:
    print('Load db:', e)
# CONSTANTS
Icon = {'n': '', 'viewed': 'Icons/viewed.png', 'not_finished': 'Icons/not_finished.ico',
    'con': 'Icons/continuation.ico', 'viewing': 'Icons/looking.ico', 'pause': 'Icons/pause.ico'}
Color = {'n': '#D9D9D9', 'edit': 'none', 'viewed': '#AEDD17', 'viewing': '#6ebcd2', 'pause': '#DC143C',
    'is_con': '#FEE02F'}
# Skin = 'Skins/dark_orange.css'
Skin = 'style.css'
SideWidth = 300
SideAnimDur = 500
AddFormDur = 500  # Add title form anim
RowAnimDur = (6, 6)  # (AnimDown,AnimUp)
RowHeightMin = 34
RowHeightMax = 72
ConListName = '*Список продолжений*'
main = [None, None]


def save_data(save, value=1):
    try:
        global ID, TotalAdded, TotalViewed
        if save == 'id':
            ID += 1
            sql.execute('UPDATE Data set value=%s where name="id"' % ID)
        if save == 'viewed':
            TotalViewed += value
            main[0].viewed_count.setText('Всего просмотрено:' + str(TotalViewed))
            sql.execute('UPDATE Data set value=%s where name="viewed"' % TotalViewed)
        if save == 'added':
            TotalAdded += value
            sql.execute('UPDATE Data set value=%s where name="added"' % TotalAdded)
        db.commit()
    except Exception as e:
        print('Main.save_data:', e)


class SelfStyledIcon(QProxyStyle):
    def pixelMetric(self, q_style_pixel_metric, option=None, widget=None):
        if q_style_pixel_metric == QStyle.PM_SmallIconSize:
            return 30
        else:
            return QProxyStyle.pixelMetric(self, q_style_pixel_metric, option, widget)


class RowButtons(QWidget):
    def __init__(self, con=False):
        super(RowButtons, self).__init__()
        try:
            self.p = None
            self.btns = QHBoxLayout(self)
            self.btns.setContentsMargins(3, 0, 3, 0)

            self.delT = QPushButton('УДАЛИТЬ')
            self.delT.setFocusPolicy(Qt.NoFocus)
            self.delT.setCursor(QCursor(Qt.PointingHandCursor))
            self.delT.clicked.connect(self.delete_title)
            if con:
                self.btns.addWidget(self.delT)
            else:
                self.row_left = QHBoxLayout()
                self.row_left.setAlignment(Qt.AlignLeft)
                self.row_right = QHBoxLayout()
                self.row_right.setAlignment(Qt.AlignRight)

                self.viewing = QPushButton('СМОТРЮ')
                self.viewing.setFixedSize(115, 30)
                self.viewing.setFocusPolicy(Qt.NoFocus)
                self.viewing.setCursor(QCursor(Qt.PointingHandCursor))
                self.viewing.clicked.connect(self.viewing_now)

                self.viewed = QPushButton('ПРОСМОТРЕНО')
                self.viewed.setFixedSize(170, 30)
                self.viewed.setFocusPolicy(Qt.NoFocus)
                self.viewed.setCursor(QCursor(Qt.PointingHandCursor))
                self.viewed.clicked.connect(self.select_mark)

                self.delT.setFixedSize(90, 30)

                self.row_left.addWidget(self.viewing)
                self.row_left.addWidget(self.viewed)
                self.row_right.addWidget(self.delT)
                self.btns.addLayout(self.row_left)
                self.btns.addLayout(self.row_right)

                self.date = QLineEdit(strftime('%Y'), self)
                self.date.setAlignment(Qt.AlignCenter)
                self.date.setGeometry(123, 0, 170, 30)
                self.date.hide()
                self.date.focusOutEvent = lambda x: self.date.hide()
                self.date.returnPressed.connect(self.set_con_date)
        except Exception as e:
            print('Row_Buttons:', e)

    def viewing_now(self):
        try:
            self.p.leave(False)
            if self.p.icon == 'viewing':
                self.p.set_color('n')
                self.p.set_icon('n')
                self.viewing.setText('СМОТРЮ')
                main[1].sideBar.load_side_data(self.p.id)
            else:
                self.p.set_color('viewing')
                self.p.set_icon('viewing')
                self.viewing.setText('НЕ СМОТРЮ')
                main[1].sideBar.load_side_data(self.p.id)
        except Exception as e:
            print('viewing_now:', e)

    def delete_title(self):
        self.p.delete_title()

    def set_con_date(self):
        if self.p.color not in ['is_con', 'viewed']:
            save_data('viewed')
        self.p.set_icon('con')
        self.p.set_color('viewed')
        self.date.hide()
        sql.execute('update titles set date="%s" where id=%s' % (self.date.text(), self.p.id))
        db.commit()
        try:
            if ConListName in main[0].tabMap:
                tab = main[0].tabWidget.widget(main[0].tabMap.index(ConListName))
                name = self.p.title_name.text()
                count = self.p.count.text()
                id_ = self.p.id
                date = self.date.text()
                tab.add_row(name, count, id_, date)
        except Exception as e:
            print('set_con_date:', e)

    def select_mark(self):
        try:
            menu = QMenu(self)

            ico = QIcon('Icons/viewed.png')
            on_viewed = menu.addAction(ico, 'Просмотрен')
            on_viewed.setEnabled(self.p.icon != 'viewed')

            ico = QIcon('Icons/continuation.ico')
            on_con = menu.addAction(ico, 'Будет продолжение')
            on_con.setEnabled(self.p.icon != 'con')

            ico = QIcon('Icons/pause.ico')
            on_pause = menu.addAction(ico, 'Просмотр брошен')
            on_pause.setEnabled(self.p.icon not in ['viewed', 'con'])

            cursor = QPoint(self.viewed.x(), -35)
            selected = menu.exec_(self.mapToGlobal(cursor))

            if selected == on_viewed:
                if self.p.color not in ['is_con', 'viewed']:
                    save_data('viewed')
                if self.p.icon == 'con':
                    sql.execute('''update Titles set date="n",icon="viewed" 
                                WHERE id=%s''' % self.p.id)
                self.p.set_color('viewed')
                self.p.set_icon('viewed')
            if selected == on_con:
                self.date.show()
                self.date.setFocus()
                self.date.selectAll()
                self.date.setStyleSheet('QLineEdit{font-size:16px;font-weight:bold;background:#D9D9D9}')
            if selected == on_pause:
                self.p.set_icon('pause')
                self.p.set_color('pause')

            self.p.p.sideBar.load_side_data(self.p.id)
        except Exception as e:
            print('select_mark:', e)


class AddTitleForm(QWidget):
    def __init__(self, parent):
        try:
            super(AddTitleForm, self).__init__(parent)
            loadUi('GUI/Add_Title_Form.ui', self)
            self.parent = parent
            self.hide()

            self.anim = QPropertyAnimation(self, b"size")
            self.anim.setEasingCurve(QEasingCurve.OutExpo)
            self.anim.setDuration(AddFormDur)

            self.count.setValidator(QIntValidator(0, 9999))
            self.count.returnPressed.connect(self.ok.click)

            self.title_name.returnPressed.connect(self.ok.click)
            self.cancel.clicked.connect(self.show_add_form)
            self.ok.clicked.connect(self.on_ok)  # self.is_con.stateChanged.connect(self.changed)
        except Exception as e:
            print('Add_Title_Form:', e)

    # Show/hide add form
    def show_add_form(self):
        try:
            if self.isHidden():
                self.show()
                self.title_name.setFocus()
                self.title_name.selectAll()
                self.anim.setEndValue(QSize(370, 245))
                self.anim.start()
            else:
                self.anim.stop()
                self.anim.setEndValue(QSize(370, 0))
                self.anim.start()
                QTimer.singleShot(SideAnimDur, self.close)
        except Exception as e:
            print('show_add_form:', e)

    def on_ok(self):
        try:
            name = self.title_name.text()
            count = self.count.text()
            genre = self.genre.text()
            link = self.link.text()
            desc = self.desc.toPlainText()

            if name == '':
                QMessageBox.warning(self, "PLS", "Title name is require field!")
                self.title_name.setFocus()
            elif count == '':
                QMessageBox.warning(self, "PLS", "Count is require field!")
                self.count.setFocus()
            else:
                if self.is_con.checkState() == 2:
                    color = 'is_con'
                else:
                    color = 'n'
                if self.is_finished.checkState() == 2:
                    icon = 'not_finished'
                else:
                    icon = 'n'

                self.parent.add_title(name, count, genre, link, desc, icon, color)
                self.show_add_form()
        except Exception as e:
            print('on_ok:', e)


class TabBar(QTabBar):
    def __init__(self, parent):
        super(TabBar, self).__init__(parent)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setExpanding(True)


class SideBar(QWidget):
    def __init__(self, parent):
        super(SideBar, self).__init__(parent)
        try:
            loadUi('GUI/Side_Bar.ui', self)
            self.p = parent
            self.change_check = True

            self.closeSide.clicked.connect(self.hide_show_side)

            self.genre.doubleClicked.connect(self.do_edit)
            self.genre.setCursor(QCursor(Qt.PointingHandCursor))
            self.genre.returnPressed.connect(self.save_desc)

            self.desc.doubleClicked.connect(self.do_edit)
            self.desc.setCursor(QCursor(Qt.PointingHandCursor))

            self.link.doubleClicked.connect(self.do_edit)
            self.link.setCursor(QCursor(Qt.PointingHandCursor))
            self.link.returnPressed.connect(self.save_desc)

            self.save.clicked.connect(self.save_desc)

            self.is_con.stateChanged.connect(self.on_is_con)
            self.is_finished.stateChanged.connect(self.on_is_finished)

            self.animSide = QPropertyAnimation(self, b"geometry")
            self.animSide.setEasingCurve(QEasingCurve.OutExpo)
            self.animSide.setDuration(SideAnimDur)
        except Exception as e:
            print(e)

    def save_desc(self):
        try:
            self.do_edit(False)
            genre = self.genre.text()
            link = self.link.text()
            desc = self.desc.toPlainText()
            sql.execute(
                'update titles set genre="%s",link="%s",desc="%s" where id=%s' % (genre, link, desc, self.p.curRow.id))
            db.commit()
        except Exception as e:
            print('save_desc:', e)

    def on_is_finished(self, state):
        if self.change_check:
            if state == 2:
                self.p.curRow.set_icon('not_finished')
            else:
                self.p.curRow.set_icon('n')

    def on_is_con(self, state):
        if self.change_check:
            if state == 2:
                self.p.curRow.set_color('is_con')
            else:
                self.p.curRow.set_color('n')

    # On doubleclick
    def do_edit(self, edit=True):
        self.genre.setReadOnly(not edit)
        self.link.setReadOnly(not edit)
        self.desc.setReadOnly(not edit)
        self.save.setEnabled(edit)
        if edit:
            self.genre.setCursor(QCursor(Qt.IBeamCursor))
            self.link.setCursor(QCursor(Qt.IBeamCursor))
            self.desc.setCursor(QCursor(Qt.IBeamCursor))
        else:
            self.genre.setCursor(QCursor(Qt.PointingHandCursor))
            self.link.setCursor(QCursor(Qt.PointingHandCursor))
            self.desc.setCursor(QCursor(Qt.PointingHandCursor))

    # On esc at side bar
    def keyPressEvent(self, event):
        try:
            if event == '' or event.key() == Qt.Key_Escape:
                self.genre.undo()
                self.link.undo()
                self.desc.undo()
                self.do_edit(False)
        except Exception as e:
            print('sideBar esc:', e)

    # Load and set title-data into side bar
    def load_side_data(self, t_id):
        try:
            self.do_edit(False)

            data = list(sql.execute('SELECT genre,link,desc,icon,color FROM Titles WHERE id=%s' % t_id))[0]
            self.genre.setText(data[0])
            self.link.setText(data[1])
            self.desc.setText(data[2])

            icon_state = 2 if data[3] == 'not_finished' else 0
            color_state = 2 if data[4] == 'is_con' else 0
            self.change_check = False
            self.is_con.setCheckState(color_state)
            self.is_con.setEnabled(data[3] in ['n', 'not_finished'])
            self.is_finished.setCheckState(icon_state)
            self.is_finished.setEnabled(data[3] in ['n', 'not_finished'])
            self.change_check = True
        except Exception as e:
            print("load_side_data:", e)

    # Switch hide/show side bar
    def hide_show_side(self):
        try:
            if self.p.side_hiden:
                self.animSide.setEndValue(QRect(self.p.w - SideWidth, 0, SideWidth, self.p.h))
                self.p.side_hiden = False
                self.closeSide.setText('>')
            else:
                self.animSide.setEndValue(QRect(self.p.w - 20, 0, SideWidth, self.p.h))
                self.p.side_hiden = True
                self.closeSide.setText('<')
            self.animSide.start()
        except Exception as e:
            print('SideBar/reHideSide:', e)


class NewTitle(QWidget):
    def __init__(self, parent, name, count, id_, icon, color):
        try:
            super(NewTitle, self).__init__(parent)
            loadUi('GUI/New_Title.ui', self)
            self.color = color
            self.name = name
            self.icon = icon
            self.p = parent
            self.id = id_
            self.h = RowHeightMin

            self.row_layout.setAlignment(Qt.AlignTop)

            self.title_name.setText(name)
            self.title_name.clicked.connect(self.select_row)
            self.title_name.doubleClicked.connect(self.edit_line)
            self.title_name.returnPressed.connect(self.end_line_edit)
            self.title_name.setCursor(QCursor(Qt.PointingHandCursor))

            self.count.setCursor(QCursor(Qt.PointingHandCursor))
            self.count.setValidator(QIntValidator(0, 9999))
            self.count.setText(str(count))
            self.count.returnPressed.connect(self.end_line_edit)
            self.count.clicked.connect(self.select_row)
            self.count.doubleClicked.connect(self.edit_line)

            self.con_date.clicked.connect(self.select_row)
            self.con_date.doubleClicked.connect(self.edit_line)
            self.con_date.returnPressed.connect(self.end_line_edit)
            self.con_date.setCursor(QCursor(Qt.PointingHandCursor))

            if parent.con:
                self.status.hide()
                self.con_date.setText(icon)
            else:
                self.con_date.hide()
                self.set_icon(icon)
                self.set_color(self.color, True)

            # todo: переделать по sroll_to timer...
            self.animOn = QTimer(self)
            self.animOn.timeout.connect(self.row_on)
            self.animOff = QTimer(self)
            self.animOff.timeout.connect(self.row_off)
        except Exception as e:
            print('new_title:', e)

    def delete_title(self):
        try:
            # Delete title from con list
            if self.p.con:
                sql.execute('update Titles set date="n",icon="viewed" WHERE id=%s' % self.id)
                # todo: сделать синхронинзацию при удалении из con_list
            else:
                sql.execute('DELETE FROM Titles WHERE id=%s' % self.id)
            db.commit()
            self.h = 0
            self.animOff.start(2)
            if self.color == 'viewed': save_data('viewed', -1)
            save_data('added', -1)
        except Exception as e:
            print('delete_title:', e)

    def set_icon(self, ico):
        icon = QPixmap(Icon[ico]).scaled(30, 30)
        self.status.setPixmap(icon)
        if ico != self.icon:
            self.icon = ico
            sql.execute('UPDATE Titles SET icon="%s" WHERE id=%s' % (ico, self.id))
            db.commit()

    def set_color(self, color, load=False):
        if self.color != 'is_con' or color in ('is_con', 'edit') or (
                self.color == 'is_con' and color == 'n' and self.icon in ['n', 'not_finished']):

            if load:
                self.setStyleSheet('#title_name,#count,#con_date{background: %s}' % Color[color])
            else:
                self.setStyleSheet('''
                    #title_name,#count,#con_date{background: %s}
                    #t_row{border-color: blue}
                    ''' % Color[color])

            if color not in ['edit', self.color]:
                self.color = color
                sql.execute('UPDATE Titles SET color="%s" WHERE id=%s' % (color, self.id))
                db.commit()

    # Hide/show buttons
    def set_buttons(self, show):
        if show:
            self.row_layout.addWidget(self.p.rowButns)
        elif not self.p.con:
            self.p.rowButns.viewing.setText('СМОТРЮ')
            self.p.rowButns.viewing.setEnabled(True)

    # ON click row
    def select_row(self):
        try:
            if self.p.curRow not in [self, None]:
                self.p.curRow.leave()
            if self.p.curRow is not self:
                self.setStyleSheet('''
                    #t_row{border-color: blue}
                    #title_name,#count,#con_date{background: %s}''' % Color[self.color])
                self.p.curRow = self
                self.p.sideBar.closeSide.setEnabled(True)
                self.p.sideBar.load_side_data(self.id)
                self.animOn.start(RowAnimDur[0])

                self.p.rowButns.setParent(self)
                self.p.rowButns.p = self

                if self.icon == 'viewing':
                    self.p.rowButns.viewing.setText('НЕ СМОТРЮ')
                if self.icon in ['viewed', 'con']:
                    self.p.rowButns.viewing.setEnabled(False)
        except Exception as e:
            print('select_row:', e)

    # ON doubleclick row
    def edit_line(self):
        try:
            self.title_name.setReadOnly(False)
            self.title_name.setCursor(QCursor(Qt.IBeamCursor))
            self.count.setReadOnly(False)
            self.count.setCursor(QCursor(Qt.IBeamCursor))
            self.con_date.setReadOnly(False)
            self.con_date.setCursor(QCursor(Qt.IBeamCursor))
            self.set_color('edit')

            if not self.p.side_hiden:
                self.p.sideBar.hide_show_side()
        except Exception as e:
            print('on_line_edit:', e)

    # ON enter pressed
    def end_line_edit(self):
        try:
            self.title_name.clearFocus()
            self.count.clearFocus()
            name = self.title_name.text()
            count = self.count.text()
            date = self.con_date.text()
            sql.execute('''UPDATE Titles SET title_name="%s",count=%s,date="%s"
                        WHERE id=%s''' % (name, count, date, self.id))
            db.commit()
            self.leave(False)
        except Exception as e:
            print('on_line_edited:', e)

    # ON edit ecs
    def keyPressEvent(self, event):
        try:
            if event == '' or event.key() == Qt.Key_Escape:
                self.title_name.clearFocus()
                self.title_name.undo()
                self.count.clearFocus()
                self.count.undo()
                self.con_date.undo()
                self.leave(False)
                # On esc set date of con
                if not self.p.con:
                    self.p.rowButns.date.hide()
        except Exception as e:
            print('on row edit esc:', e)

    # Anim row down
    def row_on(self):
        try:
            if self.height() < RowHeightMax:
                self.setFixedHeight(self.height() + 1)
            else:
                self.animOn.stop()
                self.set_buttons(True)
        except Exception as e:
            print('row_on:', e)

    # Anim row up
    def row_off(self):
        if self.height() > self.h:
            self.setFixedHeight(self.height() - 1)
        else:
            if self.h == 0:
                self.animOff.stop()
                self.p.rowButns.setParent(None)
                self.setParent(None)
                self.p.curRow = None
                self.h = RowHeightMin
                self.p.row_count.setText('Тайтлов в плейлисте:' + str(self.p.rowList.count()))
                del self
            else:
                self.animOff.stop()

    def anim_row(self, direction):
        def anim(direction):
            self.setFixedHeight(self.height() + direction)

        self.setFixedHeight(self.height() + direction)
        while RowHeightMin < self.height() < RowHeightMax:
            anim(direction)

    def leave(self, change=True):
        self.animOff.stop()
        self.animOn.stop()
        if change:
            # ON change row
            self.set_buttons(False)
            self.keyPressEvent('')
            self.animOff.start(RowAnimDur[1])
            self.setStyleSheet('''
            #t_row{border-color: #F0F0F0}
            QLineEdit{background: %s}
            #t_row:hover{border-color: #6ebcd2;}''' % Color[self.color])
        else:
            self.set_color(self.color)

        self.title_name.setReadOnly(True)
        self.title_name.setCursor(QCursor(Qt.PointingHandCursor))
        self.count.setReadOnly(True)
        self.count.setCursor(QCursor(Qt.PointingHandCursor))
        self.con_date.setReadOnly(True)
        self.con_date.setCursor(QCursor(Qt.PointingHandCursor))


class NewPlaylist(QWidget):
    def __init__(self, parent, name):
        super(NewPlaylist, self).__init__(parent)
        try:
            loadUi('GUI/New_Playlist.ui', self)
            self.p = parent
            self.name = name
            self.curRow = None
            self.rowMap = list()
            self.con = name == ConListName
            self.rowButns = RowButtons(self.con)

            self.rowList.setAlignment(Qt.AlignTop)
            self.bar_left.setAlignment(Qt.AlignLeft)
            self.bar_right.setAlignment(Qt.AlignRight)

            self.add_form = AddTitleForm(self)
            self.add_form.setGeometry(9, 49, 370, 0)

            self.addT.clicked.connect(self.add_form.show_add_form)
            self.delP.clicked.connect(self.delete_playlist)

            self.sideBar = SideBar(self)
            self.side_hiden = True

            self.test.clicked.connect(self._test)

            self.load_titles(name)
        except Exception as e:
            print("New_Playlist:", e)

    # TEMP
    def _test(self):
        try:
            menu = QMenu(self)

            act1 = menu.addAction('Take index')

            selected = menu.exec_(self.mapToGlobal(QPoint(0,0)))

            if selected == act1:
                self.p.refresh_tab(self)

        except Exception as e: print("_test: ", e)

    # Move scroll bar
    def scroll_to(self, index):
        try:
            bar = self.scrollArea.verticalScrollBar()
            step = bar.pageStep()
            row_size = RowHeightMin + self.rowList.spacing()
            target_pos = row_size * index + self.rowList.spacing()
            bottom_border = bar.value() + step - RowHeightMax

            def anim_scroll(direction):
                loop = QEventLoop()
                QTimer.singleShot(40, loop.quit)
                loop.exec_()
                bar.setValue(bar.value() + direction * 30)

            if target_pos < bar.value():
                while bar.value() > target_pos: anim_scroll(-1)
            elif target_pos > bottom_border:
                while bar.value() < target_pos and bar.value() < bar.maximum():
                    anim_scroll(1)
            print('scroll finished')
        except Exception as e:
            print("scroll_to: ", e)

    def resizeEvent(self, event=None):
        try:
            self.w = self.width()
            self.h = self.height()
            if self.side_hiden:
                self.sideBar.setGeometry(self.w - 20, 0, SideWidth, self.h)
            else:
                self.sideBar.setGeometry(self.w - SideWidth, 0, SideWidth, self.h)
        except Exception as e:
            print(e, "||New_P/resizeEvent")

    def delete_playlist(self):
        try:
            name = self.p.pList.currentText()
            sql.execute("DELETE FROM Playlists WHERE Name=?", [name])
            sql.execute('delete from Titles where playlist="%s"' % name)
            db.commit()
            self.p.close_tab(self.p.pList.currentIndex())
            self.p.pList.removeItem(self.p.pList.currentIndex())
        except Exception as e:
            print('delete_playlist:', e)

    def add_title(self, t_name, count, genre, link, desc, icon, color):
        try:
            tab_index = self.p.tabWidget.currentIndex()
            p_name = self.p.tabWidget.tabText(tab_index)
            sql.execute("INSERT INTO Titles VALUES ('%s',%s,%s,'%s','%s','%s','%s','%s','%s','n')" % (
            t_name, count, ID, p_name, icon, color, genre, link, desc))
            db.commit()
            self.add_row(t_name, count, ID, icon, color).select_row()
            self.row_count.setText('Тайтлов в плейлисте:' + str(self.rowList.count()))
            save_data('id')
            save_data('added')
        except Exception as e:
            print("add_title:", e)

    def add_row(self, name, count, t_id, icon, color='n'):
        try:
            row = NewTitle(self, name, count, t_id, icon, color)
            self.rowList.addWidget(row)
            self.rowMap.append(t_id)
            return row
        except Exception as e:
            print("add_row:", e)

    def load_titles(self, name):
        try:
            if self.con:
                self.addT.setFixedSize(0, 0)
                self.delP.setFixedSize(0, 0)
                titles = list(sql.execute('select title_name,count,id,date from titles where date!="n"'))
                for t in titles:
                    self.add_row(t[0], t[1], t[2], t[3])
            else:
                titles = list(sql.execute('''SELECT title_name,count,id,icon,color 
                       FROM Titles WHERE playlist="%s"''' % name))
                for t in titles:
                    self.add_row(t[0], t[1], t[2], t[3], t[4])
            self.row_count.setText('Тайтлов в плейлисте:' + str(self.rowList.count()))
        except Exception as e:
            print("load_titles:", e)

class MainForm(QMainWindow):

    def __init__(self):
        super(MainForm, self).__init__()
        loadUi('GUI/Main_Form.ui', self)

        with open(Skin) as css:
            self.setStyleSheet(css.read())
        self.SelectedTab = ""
        self.tabMap = []

        self.addP.clicked.connect(self.add_p)
        self.adv.clicked.connect(self._clear)
        self.con_list.clicked.connect(self.open_con_list)

        self.pList.activated.connect(self.select_p)

        self.pName.returnPressed.connect(self.addP.click)
        self.closePName.clicked.connect(self.keyPressEvent)

        self.tabBar = TabBar(self)
        self.tabBar.currentChanged.connect(self.select_tab)
        self.tabBar.tabCloseRequested.connect(self.close_tab)
        self.tabBar.tabMoved.connect(self.on_move_tab)
        self.tabWidget.setTabBar(self.tabBar)

        self.options.clicked.connect(self.open_options)
        self.options_frame.setVisible(False)

        self.option_anim = QPropertyAnimation(self.options_frame, b"size")
        self.option_anim.setEasingCurve(QEasingCurve.OutExpo)
        self.option_anim.setDuration(500)

        self.launch()

    # todo: options
    def open_options(self):
        try:
            menu = QMenu(self)

            ico = QIcon('Icons/continuation.ico')
            con_list = menu.addAction(ico, 'Список продолжений')

            clear = menu.addAction('Clear')

            cursor = QPoint(self.options.x() + 5, self.options.y() + 10)
            selected = menu.exec_(self.mapToGlobal(cursor))

            if selected == con_list:
                self.open_con_list()
            if selected == clear:
                self._clear()

        except Exception as e:
            print('open_options: ', e)

    def open_con_list(self):
        self.add_tab('*Список продолжений*')

    # Switch show/hide add playlist
    def add_p(self):
        if self.pName.isHidden():
            self.pName.show()
            self.closePName.show()
            self.pName.setText("PL" + str(self.pList.count() + 1))
            self.pName.setFocus()
            self.pName.selectAll()
        else:
            name = self.pName.text()
            sql.execute("INSERT INTO Playlists VALUES (?)", [(name)])
            db.commit()
            self.pList.insertItem(0, name)
            self.add_tab(name)
            self.pList.setCurrentIndex(0)
            self.pName.hide()
            self.closePName.hide()

    def add_tab(self, tab_name):
        try:
            if tab_name in self.tabMap:
                self.tabWidget.setCurrentIndex(self.tabMap.index(tab_name))
            else:
                self.tabMap.insert(0, tab_name)
                self.tabWidget.insertTab(0, NewPlaylist(self, tab_name), tab_name)
                self.tabWidget.setCurrentIndex(0)
                # tab = self.tabWidget.currentWidget()
                # tab.load_titles(tab_name)
        except Exception as e:
            print('add_tab:', e)

    def close_tab(self, index):
        try:
            self.tabMap.remove(self.tabWidget.tabText(index))
            self.tabWidget.removeTab(index)
        except Exception as e:
            print('close_tab', e)

    def select_p(self):
        if self.SelectedTab != self.pList.currentText():
            self.SelectedTab = self.pList.currentText()
            self.add_tab(self.SelectedTab)

    def select_tab(self, index):
        try:
            if index >= 0:
                text = self.tabWidget.tabText(index)
                index = self.pList.findText(text)
                self.pList.setCurrentIndex(index)
                main[1] = self.tabWidget.currentWidget()
                self.SelectedTab = text
            else:
                self.SelectedTab = ""
        except Exception as e:
            print("select_tab:", e)

    def on_move_tab(self, index):
        Tab = self.tabWidget.tabText(index)
        self.tabMap.remove(Tab)
        self.tabMap.insert(index, Tab)

    # Temp
    def _clear(self):
        try:
            action = QMessageBox.question(self, "Message", "Sure?", QMessageBox.Yes | QMessageBox.No)
            if action == QMessageBox.No: return
            sql.execute("DELETE FROM Playlists")
            sql.execute("DELETE FROM Titles")
            sql.execute('UPDATE Data SET value="0"')
            db.commit()
            self.pList.clear()
            self.tabWidget.clear()
            self.tabMap.clear()
            global ID
            ID = 0
        except Exception as e:
            print(e)

    def keyPressEvent(self, event):
        try:
            if not event or (event.key() == Qt.Key_Escape and self.pName.isVisible()):
                self.pName.hide()
                self.closePName.hide()
        except Exception as e:
            print('on esc:', e)

    def launch(self):
        main[0] = self
        self.pName.hide()
        self.closePName.hide()
        load = list(sql.execute("SELECT * FROM Playlists ORDER BY rowid desc"))
        self.pList.addItems([row[0] for row in load])
        self.select_p()
        self.viewed_count.setText('Всего просмотрено:' + str(TotalViewed))
        print(">>>'Launched'")


app = QApplication(sys.argv)
app.setStyle(SelfStyledIcon('Fusion'))
exe = MainForm()
exe.show()
sys.exit(app.exec_())
