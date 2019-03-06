from sys import argv as sys_args
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication

Icons = {
    "Cross": "icons/cross.png",
    "Cross_win": "icons/cross_win.png",
    "Circle": "icons/circle.png",
    "Circle_win": "icons/circle_win.png",
    "empty": "icons/empty.png"
}
IconSize = 0.7

class Cell(QPushButton):
    def __init__(self, parent, index):
        super().__init__(parent)
        self.p = parent
        self.index = index
        self.is_empty = True
        self.state = index

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clicked.connect(self.action)

        icon = QIcon()
        icon.addPixmap(QPixmap(Icons["empty"]), QIcon.Normal)
        self.setIcon(icon)

    def action(self):
        try:
            if self.is_empty:
                self.is_empty = False
                self.state = self.p.currentPlayer
                self.setIcon(QIcon(Icons[self.p.currentPlayer]))
                self.clearFocus()
                self.p.make_step()
        except Exception as e:
            print(e)

    def resizeEvent(self, event, *args, **kwargs):
        try:
            self.setIconSize(QSize(self.width() * IconSize, self.height() * IconSize))
        except Exception as e:
            print(e)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.cells = list()
        loadUi("gui/Field.ui", self)
        self.init_field()
        self.currentPlayer = "Cross"
        self.steps_left = 9
        self.current.setText("Current player: " + self.currentPlayer)
        self.restart.clicked.connect(self.restart_game)

    def init_field(self):
        for index in range(9):
            cell = Cell(self, index)
            self.field.addWidget(cell, index // 3, index % 3)
            self.cells.append(cell)

    def restart_game(self):
        try:
            self.cells.clear()
            self.init_field()
            self.currentPlayer = "Cross"
            self.current.setText("Current player: " + self.currentPlayer)
            self.steps_left = 9
        except Exception as e:
            print(e)

    def make_step(self):
        if self.check_win():
            QMessageBox().information(self, "Win!", "%s won!" % self.currentPlayer)
            return self.restart_game()
        if self.steps_left == 1:
            QMessageBox().information(self, "Draw!", "It's draw!")
            return self.restart_game()
        self.steps_left -= 1
        self.currentPlayer = "Circle" if self.currentPlayer == "Cross" else "Cross"
        self.current.setText("Current player: " + self.currentPlayer)

    def check_win(self):
        try:
            cells = self.cells
            win_indexes = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
            ]
            for pos in win_indexes:
                if cells[pos[0]].state == cells[pos[1]].state == cells[pos[2]].state:
                    icon = QIcon(Icons[self.currentPlayer + "_win"])
                    cells[pos[0]].setIcon(icon)
                    cells[pos[1]].setIcon(icon)
                    cells[pos[2]].setIcon(icon)
                    return True
            return False
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys_args)
    form = Main()
    form.show()
    app.exec_()
