# -*- coding: utf-8 -*-
import os
import sqlite3
import sys
from datetime import datetime

from PyQt5.QtCore import QEventLoop, QTimer, Qt, QPoint, QPropertyAnimation, QEasingCurve, QSize, QRect
from PyQt5.QtGui import QIntValidator, QCursor, QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox, QProxyStyle, QWidget, QHBoxLayout, QPushButton, QMenu, QTabBar, QMainWindow, \
    QApplication, QLineEdit, QStyle
from PyQt5.uic import loadUi

# LOAD DB
try:
    if not os.path.exists("Data.pls"):
        db = sqlite3.connect("Data.pls")
        sql = db.cursor().execute
        sql("CREATE TABLE Playlists (name varchar(100))")
        sql('CREATE TABLE Data (name varchar(10),value varchar(40))')
        sql("""
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
        sql('INSERT INTO Data VALUES("id","0")')
        sql('INSERT INTO Data VALUES("viewed","0")')
        sql('INSERT INTO Data VALUES("added","0")')
        db.commit()
    else:
        db = sqlite3.connect("Data.pls")
        sql = db.cursor().execute

    data = [int(d[0]) for d in sql('SELECT value FROM Data')]
    ID = data[0]
    TotalViewed = data[1]
    TotalAdded = data[2]
except Exception as e:
    print('Load db:', e)
# CONSTANTS
Icon = {
    'n': '',
    'viewed': 'Icons/viewed.png',
    'not_finished': 'Icons/not_finished.ico',
    'con': 'Icons/continuation.ico',
    'viewing': 'Icons/looking.ico',
    'pause': 'Icons/pause.ico'}
Color = {
    'n': '#D9D9D9',
    'edit': 'none',
    'viewed': '#AEDD17',
    'viewing': '#6ebcd2',
    'pause': '#DC143C',
    'is_con': '#FEE02F'}
# Skin = 'Skins/dark_orange.css'
Skin = 'style.css'
SideWidth = 300
SideAnimDur = 500
AddFormDur = 500  # Add title form anim
RowAnimDur = (6, 6)  # (AnimDown,AnimUp)
RowLoadDur = 20
RowHeightMin = 34
RowHeightMax = 72
ScrollDur = 1000
ConListName = '*Список продолжений*'
MainP = None
TitlesSortBy = "count"


# todo: to static
def save_data(save, value=1):
    try:
        global ID, TotalAdded, TotalViewed
        if save == 'id':
            ID += 1
            sql('UPDATE Data set value=%s where name="id"' % ID)
        if save == 'viewed':
            TotalViewed += value
            MainP.viewed_count.setText('Всего просмотрено:' + str(TotalViewed))
            sql('UPDATE Data set value=%s where name="viewed"' % TotalViewed)
        if save == 'added':
            TotalAdded += value
            sql('UPDATE Data set value=%s where name="added"' % TotalAdded)
        db.commit()
    except Exception as e:
        QMessageBox.critical(MainP, "PLS4_ERROR: __main__save_data", str(e))


class SelfStyledIcon(QProxyStyle):
    def pixelMetric(self, q_style_pixel_metric, option=None, widget=None):
        if q_style_pixel_metric == QStyle.PM_SmallIconSize:
            return 30
        else:
            return QProxyStyle.pixelMetric(self, q_style_pixel_metric, option, widget)


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
            QMessageBox.critical(self, "PLS4_ERROR: SideBar__init", str(e))

    def save_desc(self):
        try:
            self.do_edit(False)
            genre = self.genre.text()
            link = self.link.text()
            desc = self.desc.toPlainText()
            sql(
                'update titles set genre="%s",link="%s",desc="%s" where id=%s' % (genre, link, desc, self.p.curRow.id))
            db.commit()
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: save_desc", str(e))

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
            QMessageBox.critical(self, "PLS4_ERROR: sideBar_esc", str(e))

    # Load and set title-data into side bar
    def load_side_data(self, t_id):
        try:
            self.do_edit(False)

            data = list(sql('SELECT genre,link,desc,icon,color FROM Titles WHERE id=%s' % t_id))[0]
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
            QMessageBox.critical(self, "PLS4_ERROR: load_side_data", str(e))

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
            QMessageBox.critical(self, "PLS4_ERROR: hide_show_sidebar", str(e))


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

                data = datetime.today().strftime('%Y')
                self.date = QLineEdit(data, self)
                self.date.setAlignment(Qt.AlignCenter)
                self.date.setGeometry(123, 0, 170, 30)
                self.date.hide()
                self.date.focusOutEvent = lambda x: self.date.hide()
                self.date.returnPressed.connect(self.set_con_date)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: RowButtons__init", str(e))

    def viewing_now(self):
        try:
            self.p.leave(False)
            if self.p.icon == 'viewing':
                self.p.set_color('n')
                self.p.set_icon('n')
                self.viewing.setText('СМОТРЮ')
                self.p.p.sideBar.load_side_data(self.p.id)
            else:
                self.p.set_color('viewing')
                self.p.set_icon('viewing')
                self.viewing.setText('НЕ СМОТРЮ')
                self.p.p.sideBar.load_side_data(self.p.id)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: viewing_now", str(e))

    def delete_title(self):
        self.p.delete_title()

    def set_con_date(self):
        try:
            if self.p.color not in ['is_con', 'viewed']:
                save_data('viewed')
            self.p.set_icon('con')
            self.p.set_color('viewed')
            self.date.hide()
            sql('update titles set date="%s" where id=%s' % (self.date.text(), self.p.id))
            db.commit()

            if ConListName in MainP.tabMap:
                tab = MainP.tabWidget.widget(MainP.tabMap.index(ConListName))
                name = self.p.title_name.text()
                count = self.p.count.text()
                id_ = self.p.id
                date = self.date.text()
                tab.add_row(name, count, id_, date, 'n')
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: set_con_date", str(e))

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
                    sql('''update Titles set date="n",icon="viewed" 
                                WHERE id=%s''' % self.p.id)
                self.p.set_color('viewed')
                self.p.set_icon('viewed')
            if selected == on_con:
                self.date.show()
                self.date.setFocus()
                self.date.selectAll()
                self.date.setStyleSheet(
                    'QLineEdit{font-size:16px;font-weight:bold;background:#D9D9D9}')
            if selected == on_pause:
                self.p.set_icon('pause')
                self.p.set_color('pause')

            self.p.p.sideBar.load_side_data(self.p.id)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: select_mark", str(e))


class NewTitle(QWidget):
    def __init__(self, parent, name, count, id_, icon, color):
        try:
            super(NewTitle, self).__init__(parent)
            loadUi('GUI/New_Title.ui', self)
            self.id = id_
            self.p = parent
            self.icon = icon
            self.name = name
            self.color = color
            self.borderColor = "blue"
            self.hoverColor = "#6ebcd2"

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

            self.min_height = RowHeightMin
            self.animOn = QTimer(self)
            self.animOn.timeout.connect(self.anim_down)
            self.animOff = QTimer(self)
            self.animOff.timeout.connect(self.anim_up)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: NewTitle__init", str(e))

    def delete_title(self):
        try:
            # Delete title from con list
            if self.p.con:
                sql('update Titles set date="n",icon="viewed" WHERE id=%s' % self.id)
                # todo: сделать синхронинзацию при удалении из con_list
            else:
                sql('DELETE FROM Titles WHERE id=%s' % self.id)
            db.commit()
            self.min_height = 0
            self.animOff.start(2)
            self.p.row_count.setText('Тайтлов в плейлисте:' + str(self.p.rowList.count()))
            if self.color == 'viewed': save_data('viewed', -1)
            save_data('added', -1)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: delete_title", str(e))

    def set_icon(self, ico):
        icon = QPixmap(Icon[ico]).scaled(30, 30)
        self.status.setPixmap(icon)
        if ico != self.icon:
            self.icon = ico
            sql('UPDATE Titles SET icon="%s" WHERE id=%s' % (ico, self.id))
            db.commit()

    def set_color(self, color, load=False):
        if self.color != 'is_con' or color in ('is_con', 'edit') or (
                self.color == 'is_con' and color == 'n' and self.icon in ['n', 'not_finished']):
            if load:
                self.setStyleSheet('''
                #title_name,#count,#con_date{background: %s}''' % Color[color])
            else:
                self.setStyleSheet('''
                    #title_name,#count,#con_date{background: %s}
                    #t_row{border-color: %s}
                    ''' % (Color[color], self.borderColor))

            if color not in ['edit', self.color]:
                self.color = color
                sql('UPDATE Titles SET color="%s" WHERE id=%s' % (color, self.id))
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
                    #t_row{border-color: %s}
                    #title_name,#count,#con_date{background: %s}
                    ''' % (self.borderColor, Color[self.color]))
                self.p.curRow = self
                self.p.sideBar.closeSide.setEnabled(True)
                self.p.sideBar.load_side_data(self.id)
                self.animOn.start(RowAnimDur[0])

                self.p.rowButns.setParent(self)
                self.p.rowButns.p = self

                self.p.scroll_to(self.p.rowMap.index(self.id))

                if self.icon == 'viewing':
                    self.p.rowButns.viewing.setText('НЕ СМОТРЮ')
                if self.icon in ['viewed', 'con']:
                    self.p.rowButns.viewing.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: select_row", str(e))

    # ON doubleclick row
    def edit_line(self):
        try:
            self.set_edit()
            self.set_color('edit')

            if not self.p.side_hiden:
                self.p.sideBar.hide_show_side()
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: on_line_edit", str(e))

    # ON enter pressed
    def end_line_edit(self):
        try:
            self.title_name.clearFocus()
            self.count.clearFocus()
            name = self.title_name.text()
            count = self.count.text()
            date = self.con_date.text()
            sql('''UPDATE Titles SET title_name="%s",count=%s,date="%s"
                        WHERE id=%s''' % (name, count, date, self.id))
            db.commit()
            self.leave(False)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: on_line_edited", str(e))

    def set_edit(self, edit=True):
        self.title_name.setReadOnly(not edit)
        self.count.setReadOnly(not edit)
        self.con_date.setReadOnly(not edit)
        if edit:
            self.title_name.setCursor(QCursor(Qt.IBeamCursor))
            self.count.setCursor(QCursor(Qt.IBeamCursor))
            self.con_date.setCursor(QCursor(Qt.IBeamCursor))
        else:
            self.title_name.setCursor(QCursor(Qt.PointingHandCursor))
            self.count.setCursor(QCursor(Qt.PointingHandCursor))
            self.con_date.setCursor(QCursor(Qt.PointingHandCursor))

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
            QMessageBox.critical(self, "PLS4_ERROR: row_edit_esc", str(e))

    # Anim row down
    def anim_down(self):
        try:
            if self.height() < RowHeightMax:
                self.setFixedHeight(self.height() + 1)
            else:
                self.animOn.stop()
                self.set_buttons(True)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: anim_down", str(e))

    # Anim row up
    def anim_up(self):
        if self.height() > self.min_height:
            self.setFixedHeight(self.height() - 1)
        else:
            if self.min_height == 0:
                self.animOff.stop()
                self.p.rowButns.setParent(None)
                self.setParent(None)
                self.p.curRow = None
                del self
            else:
                self.animOff.stop()

    def leave(self, change=True):
        self.animOff.stop()
        self.animOn.stop()
        if change:
            self.set_buttons(False)
            self.keyPressEvent('')
            self.animOff.start(RowAnimDur[1])
            self.setStyleSheet('''
            #t_row{border-color: #F0F0F0}
            QLineEdit{background: %s}
            #t_row:hover{border-color: %s;}''' % (Color[self.color], self.hoverColor))
        else:
            self.set_color(self.color)
        self.set_edit(False)


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

            QTimer.singleShot(1, self.load_titles)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: NewPlaylist__init", str(e))

    # TEMP
    def _test(self):
        try:
            menu = QMenu(self)

            act1 = menu.addAction('Take index')

            selected = menu.exec_(self.mapToGlobal(QPoint(0, 0)))

            if selected == act1:
                self.scroll_to(13)

        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: _test", str(e))

    # Move scroll bar
    def scroll_to(self, index: int):
        try:
            bar = self.scrollArea.verticalScrollBar()
            step = bar.pageStep()
            row_size = RowHeightMin + self.rowList.spacing()
            target_pos = row_size * index + self.rowList.spacing()
            bottom_border = bar.value() + step - RowHeightMax
            anim_step = abs(target_pos - bar.value()) * 0.09
            print(anim_step)

            def anim_scroll(anim_step):
                anim_step = 1 if anim_step == 0 else anim_step
                loop = QEventLoop()
                QTimer.singleShot(40, loop.quit)
                loop.exec_()
                bar.setValue(bar.value() + anim_step)

            if target_pos < bar.value():
                while bar.value() > target_pos: anim_scroll(-anim_step)
            elif target_pos > bottom_border:
                while bar.value() < target_pos and bar.value() < bar.maximum():
                    anim_scroll(anim_step)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: scroll_to", str(e))

    def resizeEvent(self, event=None):
        try:
            self.w = self.width()
            self.h = self.height()
            if self.side_hiden:
                self.sideBar.setGeometry(self.w - 20, 0, SideWidth, self.h)
            else:
                self.sideBar.setGeometry(self.w - SideWidth, 0, SideWidth, self.h)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: NewPlaylist_resizeEvent", str(e))

    def delete_playlist(self):
        try:
            name = self.p.pList.currentText()
            sql("DELETE FROM Playlists WHERE Name=?", [name])
            sql('delete from Titles where playlist="%s"' % name)
            db.commit()
            self.p.close_tab(self.p.pList.currentIndex())
            self.p.pList.removeItem(self.p.pList.currentIndex())
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: delete_playlist", str(e))

    def add_title(self, t_name, count, genre, link, desc, icon, color):
        try:
            # tab_index = self.p.tabWidget.currentIndex()

            sql("INSERT INTO Titles VALUES ('%s',%s,%s,'%s','%s','%s','%s','%s','%s','')"
                % (t_name, count, ID, self.name, icon, color, genre, link, desc))
            db.commit()
            row_id = list(sql("""SELECT id, {1} FROM Titles 
                                 WHERE playlist = '{0}' ORDER BY {1}
                              """.format(self.name, TitlesSortBy)))
            for i in range(len(row_id)):
                if row_id[i][0] == ID:
                    row_id = i
                    break

            self.add_row(t_name, count, ID, icon, color, row_id).select_row()
            self.row_count.setText('Тайтлов в плейлисте:' + str(self.rowList.count()))
            save_data('id')
            save_data('added')
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: add_title", str(e))

    # todo: anim it по формуле
    def add_row(self, name, count, t_id, icon_date, color, index=0, row_count=1):
        try:
            row = NewTitle(self, name, count, t_id, icon_date, color)
            index = index if index > 0 else self.rowList.count()
            delay = 20

            self.rowList.insertWidget(index, row)
            self.rowMap.insert(index, t_id)
            loop = QEventLoop()
            QTimer.singleShot(delay, loop.quit)
            loop.exec_()
            return row
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: add_row", str(e))

    def load_titles(self):
        try:
            if self.con:
                self.addT.setFixedSize(0, 0)
                self.delP.setFixedSize(0, 0)

                titles = list(sql(
                    'select title_name,count,id,date from titles where date!=""'))
                for t in titles:
                    self.add_row(t[0], t[1], t[2], t[3], 'n', len(titles))
            else:
                titles = list(sql('''SELECT title_name,count,id,icon,color 
                                     FROM Titles WHERE playlist="%s" ORDER BY %s
                                     ''' % (self.name, TitlesSortBy)))
                for t in titles:
                    self.add_row(t[0], t[1], t[2], t[3], t[4], len(titles))
            self.row_count.setText('Тайтлов в плейлисте:' + str(self.rowList.count()))
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: load_titles", str(e))


class MainForm(QMainWindow):

    def __init__(self):
        super(MainForm, self).__init__()
        loadUi('GUI/Main_Form.ui', self)

        with open(Skin) as style:
            self.setStyleSheet(style.read())
        self.SelectedTab = ""
        self.tabMap = []

        self.addP.clicked.connect(self.add_playlist)
        self.adv.clicked.connect(self._clear)
        self.con_list.clicked.connect(self.open_con_list)

        self.pList.activated.connect(self.select_playlist)

        self.pName.returnPressed.connect(self.addP.click)
        self.pName.hide()
        self.closePName.clicked.connect(self.keyPressEvent)
        self.closePName.hide()

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

        QTimer.singleShot(1, self.launch)

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
            QMessageBox.critical(self, "PLS4_ERROR: open_options", str(e))

    def open_con_list(self):
        self.add_tab('*Список продолжений*')

    # Show/hide add playlist
    def add_playlist(self):
        try:
            if self.pName.isHidden():
                self.pName.show()
                self.closePName.show()
                self.pName.setText("PL" + str(self.pList.count() + 1))
                self.pName.setFocus()
                self.pName.selectAll()
            else:
                name = self.pName.text()
                sql("INSERT INTO Playlists VALUES ('%s')" % name)
                db.commit()
                self.pList.insertItem(0, name)
                self.add_tab(name)
                self.pList.setCurrentIndex(0)
                self.pName.hide()
                self.closePName.hide()
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: add_playlist", str(e))

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
            QMessageBox.critical(self, "PLS4_ERROR: add_tab", str(e))

    def close_tab(self, index):
        try:
            self.tabMap.remove(self.tabWidget.tabText(index))
            self.tabWidget.removeTab(index)
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: close_tab", str(e))

    def select_playlist(self):
        if self.SelectedTab != self.pList.currentText():
            self.SelectedTab = self.pList.currentText()
            self.add_tab(self.SelectedTab)

    def select_tab(self, index):
        try:
            if index >= 0:
                text = self.tabWidget.tabText(index)
                index = self.pList.findText(text)
                self.pList.setCurrentIndex(index)
                self.SelectedTab = text
            else:
                self.SelectedTab = ""
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: select_tab", str(e))

    def on_move_tab(self, index):
        Tab = self.tabWidget.tabText(index)
        self.tabMap.remove(Tab)
        self.tabMap.insert(index, Tab)

    # Temp
    def _clear(self):
        try:
            action = QMessageBox.question(self, "Message", "Sure?", QMessageBox.Yes | QMessageBox.No)
            if action == QMessageBox.No: return
            sql("DELETE FROM Playlists")
            sql("DELETE FROM Titles")
            sql('UPDATE Data SET value="0"')
            db.commit()
            self.pList.clear()
            self.tabWidget.clear()
            self.tabMap.clear()
            global ID
            ID = 0
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: _clear", str(e))

    # pl name esc
    def keyPressEvent(self, event):
        try:
            if not event or (event.key() == Qt.Key_Escape and self.pName.isVisible()):
                self.pName.hide()
                self.closePName.hide()
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: MainForm_on_esc", str(e))

    # todo: автоотслеживание тайтлов
    def check_continuations(self):
        try:
            cons = list(sql("SELECT date, id FROM Titles WHERE date != ''"))
            today = datetime.today()
            count = 0
            print(cons)
            for title in cons:
                date = title[0] if title[0] != '0' else "0001.0.0"
                date = datetime.strptime(date, "%Y.%m.%d")
                if today >= date: count += 1
            if count > 0:
                QMessageBox.information(self, 'PLS4',
                                        'Количество тайтлов получивших продолжение: %s\nОткрыть список продолжений?'
                                        % count)
        except Exception as e:
            QMessageBox.critical(self, 'PLS4_ERROR: check_continuations', str(e))

    def launch(self):
        try:
            global MainP
            MainP = self
            playlists = list(sql("SELECT * FROM Playlists ORDER BY rowid desc"))

            self.pList.addItems([row[0] for row in playlists])
            self.select_playlist()

            self.viewed_count.setText('Всего просмотрено:' + str(TotalViewed))
            self.check_continuations()
            print("Launched")
        except Exception as e:
            QMessageBox.critical(self, "PLS4_ERROR: launch", str(e))


app = QApplication(sys.argv)
app.setStyle(SelfStyledIcon('Fusion'))
exe = MainForm()
exe.show()
sys.exit(app.exec_())
