from os import mkdir as make_dir
from sys import argv as sys_args
from shutil import copy as copy_file, move as move_file
from os.path import exists as dir_exists
from sqlite3 import connect as db_connect
from requests import post as download
from subprocess import run as run_app
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QProxyStyle
from sql_extensions.exsqlite import change_columns

BasePath = r"https://github.com/Kamikoto-sama/Kamis-Code/" \
            "raw/master/Python/PlayListStore_4.0/build/"
ManifestPath = "https://github.com/Kamikoto-sama/Kamis-Code" \
               "/raw/master/Release/PLS4_Updates/"
VersionsPath = "https://github.com/Kamikoto-sama/Kamis-Code" \
               "/raw/master/Release/PLS4_Updates/versions.txt"

class Updater(QWidget):
    def __init__(self, current_version):
        super().__init__(None, Qt.WindowTitleHint)
        try:
            self.setWindowTitle("PlayListStore 4 Updating")
            self.setWindowIcon(QIcon("icons/updater.png"))
            self.setFixedSize(500, 50)
            self.setStyleSheet(open("style.css").read())
            self.bar = QProgressBar(self)
            self.bar.resize(500, 25)
            self.bar.setAlignment(Qt.AlignHCenter)
            self.bar.setTextVisible(True)
            self.status = QLabel("Loading update manifest...", self)
            self.status.setGeometry(5, 25, 250, 25)
            self.show()

            QTimer.singleShot(500, lambda: self.load_manifest(current_version))
        except Exception as e:
            print(e)

    def load_manifest(self, current_version):
        try:
            copy_file("data.pls", "save/data.pls")
            move_file("PlayListStore4.exe", "save/PlayListStore4.exe")

            versions = download(VersionsPath).text.split('=')
            if versions[-1] != current_version:
                if current_version == versions[-2]:
                    manifest = download(ManifestPath + "%s.txt" % versions[-1]).text
                    self.update(manifest)
                else:
                    for version in versions[versions.index(current_version) + 1:]:
                        manifest = download(ManifestPath + "%s.txt" % version)
                        self.update(manifest)
        except Exception as e:
            print(e)
            open("UPDATE_ERRORS.txt", 'w').write(str(e))
            self.close()

    def update(self, manifest):
        try:
            manifest = manifest.split('\n')
            modules = manifest[1:1 + int(manifest[1])]
            params = manifest[1 + int(manifest[1]):]

            self.bar.setValue(0)
            self.bar.setMaximum(len(manifest) - 1)
            for module_name in modules:
                file = download(BasePath + module_name)
                open(module_name, "wb").write(file.content)
                self.bar.setValue(self.bar.value() + 1)
                self.status.setText("Downloading: %s" % module_name)

            self.apply_params(params)
            self.close()
            run_app('PlayListStore4.exe update')
        except Exception as e:
            print(e)
            open("UPDATE_ERRORS.txt", 'w').write(str(e))
            self.close()

    def apply_params(self, params):
        param_type = None
        param_count = 0
        current_count = 0
        db = db_connect("data.pls")
        sql = db.cursor().execute
        for param in params:
            self.bar.setValue(self.bar.value() + 1)
            self.status.setText("Applying: %s" % param)

            if param_type is None or param_count == current_count:
                param = param.split()
                param_type = param[0]
                param_count = int(param[1])
                current_count = 0
                continue
            elif param_type == "change":
                param = param.split('|')
                columns = [col.split('=') for col in param[2].split(',')]
                columns = {col[0]: col[1] for col in columns}
                change_columns(db, param[1], param[0], **columns)
            elif param_type == "sql":
                sql(param)
                db.commit()
            current_count += 1
        db.close()


if __name__ == "__main__" and (not dir_exists("save") or len(sys_args) > 1):
    app = QApplication(sys_args)
    app.setStyle(QProxyStyle('Fusion'))
    args = None
    if not dir_exists("save"):
        make_dir("save")
        args = "4.0"
    if len(sys_args) > 1:
        args = sys_args[2]
    form = Updater(args)
    app.exec_()
