# -*- coding: utf-8 -*-
#import gc
import sys, os, sqlite3
from time import strftime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi

#LOAD DB
try:
    if not os.path.exists("Data.pls"):
        db = sqlite3.connect("Data.pls")
        sql = db.cursor()
        sql.execute("CREATE TABLE Playlists (name varchar(100))")
        sql.execute("CREATE TABLE Data (name varchar(10),value varchar(40))")
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
            description text,
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
except Exception as e:print('Load db:',e)
#CONSTANTS
Icon = {
    'n':'',
    'viewed':'Icons/viewed.png',
    'not_finished':'Icons/not_finished.ico',
    'con':'Icons/continuation.ico',
    'viewing':'Icons/looking.ico',
    'pause':'Icons/pause.ico'
}
Color = {
    'n':'#D9D9D9',
    'edit':'none',
    'viewed':'#AEDD17',
    'viewing':'#6ebcd2',
    'pause':'#DC143C',
    'is_con':'#FFE100'
}
#Skin = 'Skins/dark_orange.css'
Skin = 'style.css'
SideWidth = 300
SideAnimDur = 500
AddFormDur = 500    # Add title form anim
RowAnimDur = (6,6) # (AnimDown,Animup)
Parents = [None,None,None]

def save_data(save, parent=None, value=1):
    try:
        global ID, TotalAdded, TotalViewed
        if save == 'id':
            ID += 1
            sql.execute('UPDATE Data set value=%s where name="id"' % ID)
        if save == 'viewed':
            TotalViewed += value
            parent.viewed_count.setText('Всего просмотрено:' + str(TotalViewed))
            sql.execute('UPDATE Data set value=%s where name="viewed"' % TotalViewed)
        if save == 'added':
            TotalAdded += value
            sql.execute('UPDATE Data set value=%s where name="added"' % TotalAdded)
        db.commit()
    except Exception as e:print('Main.save_data:', e)


class Row_Buttons(QtWidgets.QWidget):
    def __init__(self):
        super(Row_Buttons,self).__init__()
        try:
            loadUi('GUI/Row_Buttons.ui',self)
            self.row_left.setAlignment(QtCore.Qt.AlignLeft)
            self.row_right.setAlignment(QtCore.Qt.AlignRight)

            self.viewed.clicked.connect(self.select_mark)

            self.date = QtWidgets.QLineEdit(strftime('%Y'), self)
            self.date.setAlignment(QtCore.Qt.AlignCenter)
            self.date.setGeometry(123, 0, 170, 30)
            self.date.hide()
            self.date.focusOutEvent = lambda x: self.date.hide()
            self.date.returnPressed.connect(self.set_con_date)
        except Exception as e:print('Row_Buttons:',e)

    def set_parent(self, parent):
        self.p = parent

    def set_con_date(self):
        if self.p.color not in ['is_con', 'viewed']:
            save_data('viewed', self.p.p.parent)
        self.p.set_icon('con')
        self.p.set_color('viewed')
        self.date.hide()

    def select_mark(self):
        try:
            menu = QtWidgets.QMenu(self)

            ico = QtGui.QIcon('Icons/viewed.png')
            on_viewed = menu.addAction(ico,'Просмотрен')
            on_viewed.setEnabled(self.p.icon != 'viewed')

            ico = QtGui.QIcon('Icons/continuation.ico')
            on_con = menu.addAction(ico,'Будет продолжение')
            on_con.setEnabled(self.p.icon != 'con')

            ico = QtGui.QIcon('Icons/pause.ico')
            on_pause = menu.addAction(ico,'Просмотр брошен')
            on_pause.setEnabled(self.p.icon not in ['viewed','con'])

            cursor = QtCore.QPoint(self.viewed.x(), -35)
            act = menu.exec_(self.mapToGlobal(cursor))

            if act == on_viewed:
                if self.p.color not in ['is_con','viewed']:
                    save_data('viewed', self.p.p.parent)
                self.p.set_icon('viewed')
                self.p.set_color('viewed')
            if act == on_con:
                self.date.show()
                self.date.setFocus()
                self.date.selectAll()
                self.date.setStyleSheet(
                    'QLineEdit{font-size:16px;font-weight:bold;background:#D9D9D9}')
            if act == on_pause:
                self.p.set_icon('pause')
                self.p.set_color('pause')

        except Exception as e:print('select_mark:',e)

class Self_Styled_Icon(QtWidgets.QProxyStyle):
    def pixelMetric(self, q_style_pixel_metric, option=None, widget=None):
        if q_style_pixel_metric == QtWidgets.QStyle.PM_SmallIconSize: return 30
        else:
            return QtWidgets.QProxyStyle.pixelMetric(self, q_style_pixel_metric,
                                                        option, widget)

class Add_Title_Form(QtWidgets.QWidget):
    def __init__(self,parent):
        try:
            super(Add_Title_Form,self).__init__(parent)
            loadUi('GUI/Add_Title_Form.ui',self)
            self.parent = parent
            self.hide()

            self.anim = QtCore.QPropertyAnimation(self,b"size")
            self.anim.setEasingCurve(QtCore.QEasingCurve.OutExpo)
            self.anim.setDuration(AddFormDur)

            self.count.setValidator(QtGui.QIntValidator(0,9999))
            self.count.returnPressed.connect(self.ok.click)

            self.title_name.returnPressed.connect(self.ok.click)
            self.cancel.clicked.connect(self.show_add_form)
            self.ok.clicked.connect(self.on_ok)
            #self.is_con.stateChanged.connect(self.changed)
        except Exception as e:print('Add_Title_Form:',e)
    
    # Show/hide add form
    def show_add_form(self):
        try:
            if self.isHidden():
                self.show()
                self.title_name.setFocus()
                self.title_name.selectAll()
                self.anim.setEndValue(QtCore.QSize(370,245))
                self.anim.start()
            else:
                self.anim.stop()
                self.anim.setEndValue(QtCore.QSize(370,0))
                self.anim.start()
                QtCore.QTimer.singleShot(SideAnimDur,self.close)
        except Exception as e:print('show_add_form:',e)

    def on_ok(self):
        try:
            name = self.title_name.text()
            count = self.count.text()
            genre = self.genre.text()
            link = self.link.text()
            description = self.desc.toPlainText()

            if name =='':
                QtWidgets.QMessageBox.warning(
                    self,"PLS","Title name is require field!")
                self.title_name.setFocus()
            elif count =='':
                QtWidgets.QMessageBox.warning(
                    self,"PLS","Count is require field!")
                self.count.setFocus()
            else:
                if self.is_con.checkState() == 2: color = 'is_con'
                else: color = 'n'
                if self.is_finish.checkState() == 2: icon = 'not_finished'
                else: icon = 'n'

                self.parent.add_title(name,count,genre,link,description,icon,color)
                self.show_add_form()
        except Exception as e:print('on_ok:',e)

class Tab_Bar(QtWidgets.QTabBar):
    def __init__(self,parent):
        super(Tab_Bar,self).__init__(parent)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setExpanding(True)

class Side_Bar(QtWidgets.QWidget):
    def __init__(self,parent):
        super(Side_Bar,self).__init__(parent)
        try:
            loadUi('GUI/Side_Bar.ui',self)
            self.parent = parent

            self.closeSide.clicked.connect(self.hide_show_side)

            self.animSide = QtCore.QPropertyAnimation(self,b"geometry")
            self.animSide.setEasingCurve(QtCore.QEasingCurve.OutExpo)
            self.animSide.setDuration(SideAnimDur)
        except Exception as e :print(e)

    # Load and set title-data into side bar
    def load_side_data(self, t_id):
        try:
            data = list(sql.execute(
                'SELECT genre,link,description,icon,color FROM Titles WHERE id=%s' %t_id))[0]
            self.genre.setText(data[0])
            self.link.setText(data[1])
            self.desc.setText(data[2])
            icon_state = 2 if data[3] == 'not_finished' else 0
            color_state = 2 if data[4] == 'is_con' else 0
            self.is_con.setCheckState(color_state)
            self.is_finish.setCheckState(icon_state)
        except Exception as e : print("load_side_data:",e)

    # Switch hide/show side bar
    def hide_show_side(self):
        try:
            if self.parent.side_hiden:
                self.animSide.setEndValue(QtCore.QRect(self.parent.w-SideWidth,0,
                                          SideWidth,self.parent.h))
                self.parent.side_hiden = False
                self.closeSide.setText('>')
            else:
                self.animSide.setEndValue(QtCore.QRect(self.parent.w-20,0,
                    SideWidth,self.parent.h))
                self.parent.side_hiden = True
                self.closeSide.setText('<')
            self.animSide.start()
        except Exception as e: print('SideBar/reHideSide:',e)

class New_Title(QtWidgets.QWidget):
    def __init__(self,p,name,count,id_,icon,color):
        super(New_Title,self).__init__(p)
        loadUi('GUI/New_Title.ui',self)
        try:
            self.color = color
            self.icon = icon
            self.id = id_
            self.h = 34
            self.p = p

            self.row_layout.setAlignment(QtCore.Qt.AlignTop)

            self.title_name.setText(name)
            self.title_name.mouseDoubleClickEvent = self.on_line_edit
            self.title_name.mousePressEvent = self.on_t_select
            self.title_name.returnPressed.connect(self.on_line_edited)
            self.title_name.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

            self.count.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.count.setValidator(QtGui.QIntValidator(0,9999))
            self.count.setText(str(count))
            self.count.returnPressed.connect(self.on_line_edited)
            self.count.mouseDoubleClickEvent = self.on_line_edit
            self.count.mousePressEvent = self.on_t_select

            self.animOn = QtCore.QTimer(self)
            self.animOn.timeout.connect(self.row_on)
            self.animOff = QtCore.QTimer(self)
            self.animOff.timeout.connect(self.row_off)

            self.set_icon(icon)
            self.set_color(self.color,True)
        except Exception as e:print('new_title:',e)

    def viewing_now(self):
        self.leave(False)
        if self.icon == 'viewing':
            self.set_icon('n')
            self.set_color('n')
            self.p.rowButns.viewing.setText('СМОТРЮ')
        else:
            self.set_icon('viewing')
            self.set_color('viewing')
            self.p.rowButns.viewing.setText('НЕ СМОТРЮ')

    def delete_title(self):
        try:
            sql.execute('DELETE FROM Titles WHERE id=%s'%self.id)
            db.commit()
            self.h = 0
            self.animOff.start(2)
            if self.color == 'viewed': save_data('viewed', self.p.parent,-1)
            save_data('added', self,-1)
        except Exception as e:print('delete_title:',e)

    def set_icon(self,ico):
        icon = QtGui.QPixmap(Icon[ico]).scaled(30,30)
        self.status.setPixmap(icon)
        if ico != self.icon:
            self.icon = ico
            sql.execute('UPDATE Titles SET icon="%s" WHERE id=%s'%(ico,self.id))
            db.commit()

    def set_color(self, color, load=False):
        if self.color != 'is_con' or color in ('is_con','edit'):
            if load:
                self.setStyleSheet('#title_name,#count{background: %s}'%Color[color])
            else:
                self.setStyleSheet('''
                    #title_name,#count{background: %s}
                    #t_row{border-color: blue}
                    '''%Color[color])

            if color not in ['edit',self.color] :
                self.color = color
                sql.execute(
                    'UPDATE Titles SET color="%s" WHERE id=%s'%(color,self.id))
                db.commit()

    # Hide/show buttons
    def set_buttons(self,show):
        if show:
            self.p.rowButns.delT.clicked.connect(self.delete_title)
            self.p.rowButns.viewing.pressed.connect(self.viewing_now)
            self.row_layout.addWidget(self.p.rowButns)
        else:
            self.p.rowButns.delT.clicked.disconnect(self.delete_title)
            self.p.rowButns.viewing.pressed.disconnect(self.viewing_now)
            self.p.rowButns.viewing.setText('СМОТРЮ')
            self.p.rowButns.viewing.setEnabled(True)

    # ON click row
    def on_t_select(self,event=None):
        try:
            if self.p.currentRow not in [self, None]:
                self.p.currentRow.leave()
            self.setStyleSheet('''
                #t_row{border-color: blue}
                #title_name,#count{background: %s}'''%Color[self.color])
            self.p.currentRow = self
            self.p.sideBar.load_side_data(self.id)
            self.animOn.start(RowAnimDur[0])

            self.p.rowButns.setParent(self)
            self.p.rowButns.set_parent(self)

            if self.icon == 'viewing':
                self.p.rowButns.viewing.setText('НЕ СМОТРЮ')
            if self.icon in ['viewed','con']:
                self.p.rowButns.viewing.setEnabled(False)
            self.title_name.mousePressEvent()
        except Exception as e:print('on_t_select:',e)

    # ON doubleclick row
    def on_line_edit(self,event):
        try:
            self.title_name.setReadOnly(False)
            self.title_name.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            self.count.setReadOnly(False)
            self.count.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            self.set_color('edit')

            if not self.p.side_hiden:
                self.p.sideBar.hide_show_side()
        except Exception as e:print('on_line_edit:',e)

    # ON enter pressed
    def on_line_edited(self):
        try:
            self.title_name.clearFocus()
            self.count.clearFocus()
            name = self.title_name.text()
            count = self.count.text()
            sql.execute('''UPDATE Titles SET title_name="%s",count=%s 
                        WHERE id=%s'''% (name,count,self.id))
            db.commit()
            self.leave(False)
        except Exception as e:print(e)

    # ON edit ecs
    def keyPressEvent(self, event):
        try:
            if event == '' or event.key() == QtCore.Qt.Key_Escape:
                self.title_name.clearFocus()
                self.title_name.undo()
                self.count.clearFocus()
                self.count.undo()
                self.leave(False)
                # On esc set date of con
                self.p.rowButns.date.hide()
        except Exception as e:print('on row edit esc:',e)

    # Anim row down
    def row_on(self):
        try:
            if self.height() < 72: self.setFixedHeight(self.height()+1)
            else:
                self.animOn.stop()
                self.set_buttons(True)
        except Exception as e:print('row_on:',e)

    # Anim row up
    def row_off(self):
        if self.height() > self.h:
                self.setFixedHeight(self.height()-1)
        else:
            if self.h == 0: 
                self.animOff.stop()
                self.p.rowButns.setParent(None)
                self.setParent(None)
                self.p.currentRow = None
                self.h = 34
                self.p.row_count.setText('Тайтлов в плейлисте:' + str(self.p.rowList.count()))
                del self
            else: self.animOff.stop()

    def leave(self, change=True):
        self.animOff.stop()
        self.animOn.stop()
        if change:
            # ON change row
            self.set_buttons(False)
            self.keyPressEvent('')
            self.animOff.start(RowAnimDur[1])
            self.setStyleSheet(
            '''
            #t_row{border-color: #F0F0F0}
            QLineEdit{background: %s}
            #t_row:hover{border-color: #6ebcd2;}'''%Color[self.color])
        else: self.set_color(self.color)

        self.title_name.setReadOnly(True)
        self.title_name.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.count.setReadOnly(True)
        self.count.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

class New_Playlist(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(New_Playlist,self).__init__(parent)
        try:
            loadUi('GUI/New_Playlist.ui',self)
            self.parent = parent
            self.currentRow = None
            self.rowMap = []
            self.rowButns = Row_Buttons()

            self.rowList.setAlignment(QtCore.Qt.AlignTop)
            self.bar_left.setAlignment(QtCore.Qt.AlignLeft)
            self.bar_right.setAlignment(QtCore.Qt.AlignRight)

            self.add_form = Add_Title_Form(self)
            self.add_form.setGeometry(9,49,370,0)
            self.animAddT = QtCore.QPropertyAnimation(self.add_form,b"size")
            self.animAddT.setEasingCurve(QtCore.QEasingCurve.OutExpo)
            self.animAddT.setDuration(AddFormDur)

            self.addT.clicked.connect(self.add_form.show_add_form)
            self.delP.clicked.connect(self.delete_playlist)

            self.sideBar = Side_Bar(self)
            self.side_hiden = True

        except Exception as e: print("New_Playlist:",e)

    def resizeEvent(self,event=None):
        try:
            self.w = self.width()
            self.h = self.height()
            if self.side_hiden:
                self.sideBar.setGeometry(self.w-20,0,SideWidth,self.h)
            else:
                self.sideBar.setGeometry(self.w-SideWidth,0,SideWidth,self.h)
        except Exception as e:print(e,"||New_P/resizeEvent")

    def delete_playlist(self):
        try:
            name = self.parent.pList.currentText()
            sql.execute("DELETE FROM Playlists WHERE Name=?", [name])
            sql.execute('delete from Titles where playlist="%s"'% name)
            db.commit()
            self.parent.close_tab(self.parent.pList.currentIndex())
            self.parent.pList.removeItem(self.parent.pList.currentIndex())
        except Exception as e: print('delete_playlist:', e)

    def add_title(self,t_name,count,genre,link,description,icon,color):
        try:
            tab_index = self.parent.tabWidget.currentIndex()
            p_name = self.parent.tabWidget.tabText(tab_index)
            sql.execute("INSERT INTO Titles VALUES ('%s',%s,%s,'%s','%s','%s','%s','%s','%s','')"%
                        (t_name,count,ID,p_name,icon,color,genre,link,description))
            db.commit()
            self.add_row(t_name,count,ID,icon,color).on_t_select()
            save_data('id')
            save_data('added', self.parent)
        except Exception as e:print("add_title:",e)

    def add_row(self, name, count, t_id, icon, color):
        try:
            row = New_Title(self, name, count, t_id, icon, color)
            self.rowList.addWidget(row)
            return row
        except Exception as e:print("add_row:",e)

    def load_titles(self,name):
        try:
            titles = list(sql.execute(
             '''SELECT title_name,count,id,icon,color 
                FROM Titles WHERE playlist="%s"''' %name))

            for t in titles:
                self.add_row(t[0], t[1], t[2], t[3], t[4])
                self.rowMap.append(t[0])
            self.row_count.setText('Тайтлов в плейлисте:' + str(self.rowList.count()))
        except Exception as e: print("load_titles:",e)

class MainForm(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainForm,self).__init__()
        loadUi('GUI/Main_Form.ui',self)

        with open(Skin) as css:
            self.setStyleSheet(css.read())
        self.SelectedTab = ""
        self.tabMap = []

        self.addP.clicked.connect(self.add_p)
        self.adv.clicked.connect(self._clear)

        self.pList.activated.connect(self.select_p)

        self.pName.returnPressed.connect(self.addP.click)
        self.closePName.clicked.connect(self.keyPressEvent)

        self.tabBar = Tab_Bar(self)
        self.tabBar.currentChanged.connect(self.select_tab)
        self.tabBar.tabCloseRequested.connect(self.close_tab)
        self.tabBar.tabMoved.connect(self.on_move_tab)
        self.tabWidget.setTabBar(self.tabBar)

        self.launch()

    # Switch show/hide add playlist
    def add_p(self):
        if self.pName.isHidden():
            self.pName.show()
            self.closePName.show()
            self.pName.setText("PL"+str(self.pList.count()+1))
            self.pName.setFocus()
            self.pName.selectAll()
        else:
            name = self.pName.text()
            sql.execute("INSERT INTO Playlists VALUES (?)",[(name)])
            db.commit()
            self.pList.insertItem(0,name)
            self.add_tab(name)
            self.pList.setCurrentIndex(0)
            self.pName.hide()
            self.closePName.hide()

    def add_tab(self, tab_name):
        try:
            if tab_name in self.tabMap:
                self.tabWidget.setCurrentIndex(self.tabMap.index(tab_name))
            else:
                self.tabMap.insert(0,tab_name)
                self.tabWidget.insertTab(0,New_Playlist(self),tab_name)
                self.tabWidget.setCurrentIndex(0)
                tab = self.tabWidget.currentWidget()
                tab.load_titles(tab_name)
        except Exception as e: print('add_tab:',e)

    def close_tab(self,index):
        try:
            self.tabMap.remove(self.tabWidget.tabText(index))
            self.tabWidget.removeTab(index)
        except Exception as e: print('close_tab', e)
    def select_p(self):
        if self.SelectedTab != self.pList.currentText():
            self.SelectedTab = self.pList.currentText()
            self.add_tab(self.SelectedTab)

    def select_tab(self,index):
        try:
            if index >= 0:
                text = self.tabWidget.tabText(index)
                Index = self.pList.findText(text)
                self.pList.setCurrentIndex(Index)
                self.SelectedTab = text
            else: self.SelectedTab = ""
        except Exception as e: print("select_tab:".e)

    def on_move_tab(self,index):
        Tab = self.tabWidget.tabText(index)
        self.tabMap.remove(Tab)
        self.tabMap.insert(index,Tab)

    #Временная
    def _clear(self):
        try:
            sql.execute("DELETE FROM Playlists")
            sql.execute("DELETE FROM Titles")
            sql.execute('UPDATE Data SET value="0"')
            db.commit()
            self.pList.clear()
            self.tabWidget.clear()
            self.tabMap.clear()
            global ID
            ID = 0
        except Exception as e:print(e)

    def keyPressEvent(self, event):
        try:
            if not event or (event.key() == QtCore.Qt.Key_Escape and self.pName.isVisible()) :
                self.pName.hide()
                self.closePName.hide()
        except Exception as e:print('on esc:',e)

    def launch(self):
        global Parents
        Parents[0] = self
        self.pName.hide()
        self.closePName.hide()
        load = list(sql.execute(
            "SELECT * FROM Playlists ORDER BY rowid desc"))
        self.pList.addItems([row[0] for row in load])
        self.select_p()
        self.viewed_count.setText('Всего просмотрено:' + str(TotalViewed))
        print("\n\t'Launched'")

app = QtWidgets.QApplication(sys.argv)
app.setStyle(Self_Styled_Icon('Fusion'))
exe = MainForm()
exe.show()
print("\t'Start'\n")
sys.exit(app.exec_())