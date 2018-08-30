from PyQt5.QtWidgets import QLineEdit

class reLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(reLineEdit, self).__init__(parent)
        self.parent = parent

    def mousePressEvent(self, event):
        super(reLineEdit, self).mousePressEvent(event)
        self.parent.on_t_select()