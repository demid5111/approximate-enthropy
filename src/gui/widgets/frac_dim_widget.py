from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout


class FracDimWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        fd_max_k_label = QLabel("Max K")
        self.fd_max_k = QLineEdit("20")

        grid = QGridLayout()
        grid.addWidget(fd_max_k_label, 0, 0)
        grid.addWidget(self.fd_max_k, 0, 1)

        self.setLayout(grid)

    def get_max_k(self):
        return self.get_int_prop("fd_max_k")

    def get_int_prop (self, name):
        res = -1
        try:
            res = int(getattr(self, name).text())
        except:
            pass
        return res
