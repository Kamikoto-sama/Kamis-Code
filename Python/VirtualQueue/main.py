import sys
import pyttsx3
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Window(QWidget):
    def __init__(self, parent, number, service_index):
        super().__init__(parent)
        try:
            loadUi("gui/Window.ui", self)
            self.p = parent
            self.is_free = True
            self.title = "Window " + str(number)
            self.service = alpha[service_index]
            self.client = None
            self.display_item = None

            self.box.setTitle(self.title)
            self.client_in.clicked.connect(self.on_client_in)
            self.client_clear.clicked.connect(self.on_client_clear)
        except Exception as e:
            print("Window", e)

    def order(self, client):
        try:
            self.display_item = QListWidgetItem("%s --> %s" % (client, self.title))
            self.display_item.setTextAlignment(Qt.AlignHCenter)
            self.p.display.addItem(self.display_item)
            self.p.display.setCurrentRow(self.p.display.count() - 1)

            self.client = client
            self.setStyleSheet("QGroupBox{background: lightblue}")
            self.box.setTitle("%s -> %s" % (self.title, client))
            self.client_in.setEnabled(True)
            self.client_clear.setEnabled(True)

            # talk = pyttsx3.init()
            # talk.say("Client number. %s. go to. %s" % (client, self.title))
            # talk.runAndWait()
        except Exception as e:
            print("order", e)

    def on_client_in(self):
        try:
            self.client_in.setEnabled(False)
            self.client_clear.setEnabled(True)
            self.setStyleSheet("QGroupBox{background: lightgreen}")
            self.is_free = False
            if self.p.display.currentItem() == self.display_item:
                self.p.display.setCurrentRow(-1)
        except Exception as e:
            print("on_client_in", e)

    def on_client_clear(self):
        try:
            self.client_in.setEnabled(False)
            self.client_clear.setEnabled(False)
            self.box.setTitle(self.title)
            self.is_free = True
            self.client = None
            self.setStyleSheet("QGroupBox{background: none}")

            if self.p.display.currentItem() == self.display_item:
                self.p.display.setCurrentRow(-1)
            if self.display_item is not None:
                row = self.p.display.row(self.display_item)
                self.p.display.takeItem(row)
                self.display_item = None
            self.check_orders()
        except Exception as e:
            print("on_client_clear", e)

    def check_orders(self):
        queue = self.p.queue
        if len(queue[self.service]) > 0:
            client = queue[self.service].pop(0)
            self.order(client)


class TButton(QPushButton):
    def __init__(self, parent, name, index):
        super().__init__(name, parent)
        self.setFixedSize(120, 50)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.index = index


class Ticket(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi("gui/Ticket.ui", self)
        self.setFixedSize(200, 100)
        self.p = parent

    def mousePressEvent(self, event):
        self.hide()
        self.p.ticket_time.stop()


class Place(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowCloseButtonHint)
        loadUi("gui/Place.ui", self)
        self.windows = dict()
        self.queue = dict()
        self.client_count = 0

        self.ticket = Ticket(self)
        self.ticket.hide()
        self.ticket_anim = QPropertyAnimation(self.ticket, b"pos")
        self.ticket_anim.setEasingCurve(QEasingCurve.OutExpo)
        self.ticket_anim.setDuration(1000)
        self.ticket_time = QTimer(self)
        self.ticket_time.setInterval(1500)
        self.ticket_time.timeout.connect(self.ticket.hide)

    def init(self, services):
        try:
            win_index = 0
            for index, service in enumerate(services):
                option = TButton(self, service, index)
                option.setEnabled(services[service] > 0)
                option.clicked.connect(self.select_service)
                self.terminal.addWidget(option, index // 2, index % 2)
                for i in range(services[service]):
                    if not self.windows.get(alpha[index], False):
                        self.windows[alpha[index]] = list()
                    window = Window(self, win_index + 1, index)
                    self.windows[alpha[index]].append(window)
                    self.windows_place.addWidget(window, win_index // 3, win_index % 3)
                    win_index += 1
            self.show()
        except Exception as e:
            print("init", e)

    def select_service(self):
        service = alpha[self.sender().index]
        self.client_count += 1
        client = service + str(self.client_count)
        if not self.queue.get(service, False):
            self.queue[service] = list()
        self.queue[service].append(client)
        self.print_ticket(client)
        self.check_windows(client)

    def print_ticket(self, client):
        try:
            self.ticket.text.setText("Your number\n" + client)
            self.ticket.show()
            y = self.groupBox.pos().y() + self.groupBox.height() // 2
            y -= self.ticket.height() // 2
            x = self.groupBox.width() // 2 - self.ticket.width() // 2
            self.ticket.width()
            self.ticket_anim.setStartValue(QPoint(-self.ticket.width(), y))
            self.ticket_anim.setEndValue(QPoint(x, y))
            self.ticket_anim.start()
            self.ticket_time.start()
        except Exception as e:
            print("print_ticket", e)

    def check_windows(self, client):
        try:
            for window in self.windows[client[0]]:
                if window.client is None:
                    window.order(client)
                    self.queue[client[0]].remove(client)
                    return
        except Exception as e:
            print("check_windows", e)

    def order_window(self, window, client):
        try:
            item = QListWidgetItem("%s --> %s" % (client, window.title))
            window.order(client)
            item.setTextAlignment(Qt.AlignHCenter)
            self.display.addItem(item)
        except Exception as e:
            print("order_window", e)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


class PlaceConstructor(QMainWindow):
    def __init__(self, place):
        super().__init__(None, Qt.WindowCloseButtonHint)
        loadUi("gui/Constructor.ui", self)
        self.place = place

        self.name.returnPressed.connect(self.add_service)
        self.count.returnPressed.connect(self.add_service)
        self.count.setValidator(QIntValidator(0, 100))
        self.create_btn.clicked.connect(self.create_place)
        self.load.clicked.connect(self.load_services)
        self.services.itemDoubleClicked.connect(self.delete_service)

    def add_service(self):
        try:
            item = "%s|%s" % (self.name.text(), self.count.text())
            self.services.addItem(item)
            self.count.clear()
            self.name.clear()
            self.name.setFocus()
        except Exception as e:
            print("add_service", e)

    def delete_service(self, item):
        try:
            self.services.takeItem(self.services.row(item))
        except Exception as e:
            print("delete_service", e)

    def load_services(self):
        try:
            services = dict()
            with open("services.txt", 'r') as lines:
                lines = [s.strip() for s in lines.readlines()]
                for service in lines:
                    service = service.split('|')
                    services[service[0]] = int(service[1])
                self.close()
                self.place.init(services)
        except Exception as e:
            print("load_services", e)

    def create_place(self):
        try:
            if self.services.count() > 0:
                services = dict()
                for i in range(self.services.count()):
                    item = self.services.item(i).text().split('|')
                    services[item[0]] = int(item[1])
                self.close()
                self.place.init(services)
        except Exception as e:
            print("create_place", e)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    place = Place()
    form = PlaceConstructor(place)
    form.show()
    app.exec_()
