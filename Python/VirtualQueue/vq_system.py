import sys
from exrandom import RandomEvent
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem

Alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Emulation = False
ClientProb = 90  # percents
WaitClientDur = 3000
ClientCameProb = 70  # percents
ClientInDur = 10000


class Window(QWidget):
    def __init__(self, parent, number, service_index):
        super().__init__(parent)
        try:
            loadUi("gui/Window.ui", self)
            self.p = parent
            self.is_free = True
            self.title = "Window " + str(number)
            self.service = Alpha[service_index]
            self.client = None
            self.display_item = None

            self.box.setTitle(self.title)
            self.client_in.clicked.connect(self.on_client_in)
            self.client_clear.clicked.connect(self.on_client_clear)

            self.client_event = RandomEvent(100 - ClientCameProb, ClientCameProb)
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

            if Emulation:
                QTimer().singleShot(WaitClientDur, self.emulate)
        except Exception as e:
            print("order", e)

    def emulate(self):
        try:
            if Emulation:
                events = (self.on_client_clear, self.on_client_in)
                event = self.client_event.event()
                events[event]()
                if event:
                    QTimer().singleShot(ClientInDur, self.on_client_clear)
        except Exception as e:
            print("emulate_window", e)

    def on_client_in(self):
        try:
            self.client_in.setEnabled(False)
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
        if len(self.p.queue[self.service]) > 0:
            client = self.p.queue[self.service].pop(0)
            self.order(client)


class TButton(QPushButton):
    def __init__(self, parent, name, index):
        super().__init__(name, parent)
        self.setFixedSize(120, 50)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.index = index


class Ticket(QWidget):
    def __init__(self, parent, place):
        super().__init__(parent)
        loadUi("gui/Ticket.ui", self)
        self.setFixedSize(200, 100)
        self.p = place

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

        self.ticket = Ticket(self.groupBox, self)
        self.ticket.hide()
        self.ticket_anim = QPropertyAnimation(self.ticket, b"pos")
        self.ticket_anim.setEasingCurve(QEasingCurve.OutExpo)
        self.ticket_anim.setDuration(1000)

        self.ticket_time = QTimer(self)
        self.ticket_time.setInterval(1500)
        self.ticket_time.timeout.connect(self.ticket.hide)

        self.emulation = QTimer(self)
        self.emulation.timeout.connect(self.emulate)
        self.emulation_events = None
        self.client_event = RandomEvent(100 - ClientProb, ClientProb)

        self.switch_emul.hide()
        self.switch_emul.clicked.connect(self.switch_emulation)

        self.display.mousePressEvent = lambda _: None

    def init(self, services, emulation):
        try:
            if bool(emulation):
                self.init_emulation(services, emulation)

            win_index = 0
            for index, service in enumerate(services):
                option = TButton(self, service, index)
                option.setEnabled(services[service] > 0)
                option.clicked.connect(self.select_service)
                self.terminal.addWidget(option, index // 2, index % 2)
                for i in range(services[service]):
                    if not self.windows.get(Alpha[index], False):
                        self.windows[Alpha[index]] = list()
                    window = Window(self, win_index + 1, index)
                    self.windows[Alpha[index]].append(window)
                    self.windows_place.addWidget(window, win_index // 3, win_index % 3)
                    win_index += 1
            self.show()
            self.splitter.setSizes([self.height()//2, self.height()//2])
            self.splitter2.setSizes([self.bottom.height()//2, self.bottom.height()//2])
        except Exception as e:
            print("init", e)

    def init_emulation(self, services, delay):
        global Emulation
        Emulation = True
        self.bottom_area.setEnabled(False)
        self.ticket.setEnabled(False)

        self.switch_emul.show()
        self.emulation.setInterval(delay)
        self.emulation.start()
        events = [100 // len(services) for _ in range(len(services))]
        if not (100 / len(services)).is_integer():
            events.append(100 - sum(events))
        self.emulation_events = RandomEvent(*events, shuffle=True)

    def emulate(self):
        if self.client_event.event() and Emulation:
            index = self.emulation_events.event()
            if index == len(self.windows):
                return self.emulate()
            self.select_service(index)
            print("\rTime for client %s!" % self.client_count, end='')
        else:
            print("\rNo client ...      ", end='')

    def switch_emulation(self, turn_on):
        try:
            global Emulation
            Emulation = turn_on
            self.bottom_area.setEnabled(not turn_on)
            self.ticket.setEnabled(not turn_on)
            if turn_on:
                self.emulation.start()
                self.switch_emul.setText("    Pause emulation    ")
            else:
                self.switch_emul.setText("    Continue emulation    ")
                self.emulation.stop()
        except Exception as e:
            print("switch_emulation", e)

    def select_service(self, index):
        try:
            if isinstance(self.sender(), QPushButton):
                service = Alpha[self.sender().index]
            else:
                service = Alpha[index]

            self.client_count += 1
            client = service + str(self.client_count)
            if not self.queue.get(service, False):
                self.queue[service] = list()
            self.queue[service].append(client)

            self.print_ticket(client)
            self.check_windows(client)
        except Exception as e:
            print("select_service", e)

    def print_ticket(self, client):
        try:
            if self.groupBox.height() > 0 and self.groupBox.width() > 0:
                y = self.groupBox.height() // 2 - self.ticket.height() // 2 + 10
                x = self.groupBox.width() // 2 - self.ticket.width() // 2

                self.ticket_anim.setStartValue(QPoint(-self.ticket.width(), y))
                self.ticket_anim.setEndValue(QPoint(x, y))
                self.ticket.text.setText("Your number\n" + client)
                self.ticket.show()
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
        self.emulate.stateChanged.connect(self.set_emulation)
        self.rate.returnPressed.connect(self.load_services)
        self.add.clicked.connect(self.add_service)

    def add_service(self):
        try:
            name = self.name.text().strip()
            count = self.count.text().strip()
            if '' not in [name, count]:
                item = "%s|%s" % (name, count)
                self.services.addItem(item)
                self.name.setFocus()
                self.name.selectAll()
        except Exception as e:
            print("add_service", e)

    def delete_service(self, item):
        try:
            self.services.takeItem(self.services.row(item))
        except Exception as e:
            print("delete_service", e)

    def set_emulation(self, state):
        try:
            self.rate.setEnabled(bool(state))
            if state:
                self.rate.selectAll()
                self.rate.setFocus(True)
        except Exception as e:
            print("set_emulation", e)

    def load_services(self):
        try:
            services = dict()
            with open("services.txt", 'r') as lines:
                lines = [s.strip() for s in lines.readlines()]
                for service in lines:
                    service = service.split('|')
                    services[service[0]] = int(service[1])
                self.close()

                emulation = int(self.rate.text()) if self.emulate.checkState() else 0
                self.place.init(services, emulation)
        except Exception as e:
            print("load_services", e)

    def create_place(self):
        try:
            if 0 < self.services.count() <= len(Alpha):
                services = dict()
                for i in range(self.services.count()):
                    item = self.services.item(i).text().split('|')
                    services[item[0]] = int(item[1])
                self.close()

                emulation = int(self.rate.text()) if self.emulate.checkState() else 0
                self.place.init(services, emulation)
            elif self.services.count() > len(Alpha):
                text = "Где тут '%s' %s символ ???" % (Alpha, len(Alpha) + 1)
                QMessageBox.warning(self, 'Ohuel?', text)
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
