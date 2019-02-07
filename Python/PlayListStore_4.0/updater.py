from sqlite3 import connect as db_connect
from sys import argv
from requests import post as download
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication

BasePath = r"https://github.com/Kamikoto-sama/Kamis-Code/" \
            "raw/master/Python/PlayListStore_4.0/build/"

class Updater(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowTitleHint)
        try:
            self.setWindowTitle("PlayListStore 4 Updater")
            self.setFixedSize(500, 25)
            self.bar = QProgressBar(self)
            self.bar.resize(500, 25)
            self.bar.setAlignment(Qt.AlignHCenter)
            self.bar.setTextVisible(True)
            self.show()

            # QTimer.singleShot(1000, self.update)
        except Exception as e:
            print(e)

    def update(self):
        try:
            with open("update_manifest.pls") as manifest:
                manifest = [line.strip() for line in manifest.readlines()]
                params = manifest[1].split('|') if len(manifest[1]) > 0 else []
                modules = manifest[2:]

                work_length = len(params) + len(modules)
                self.bar.setMaximum(work_length)
                status = 0
                for module_name in modules:
                    file = download(BasePath + module_name)
                    open(module_name, "wb").write(file.content)
                    status += 1
                    self.bar.setValue(status)
                for param in params:
                    status += 1
                    self.bar.setValue(status)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(argv)
    form = Updater()
    app.exec_()