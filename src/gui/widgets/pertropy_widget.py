from PyQt5.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QHBoxLayout, QLineEdit, QCheckBox, QLabel, QGridLayout

from src.utils.supporting import CalculationType


class PertropyWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.normalize_cb = QCheckBox('Calculate h(n) = (1/(n-1))*H(n)', self)
        self.is_normalize_used = True
        self.normalize_cb.setChecked(self.is_normalize_used)
        self.normalize_cb.clicked.connect(self.toggle_normalize_cb)

        grid = QGridLayout()
        grid.addWidget(self.normalize_cb, 0, 0, 1, 2)

        self.setLayout(grid)

    def toggle_normalize_cb(self):
        self.is_normalize_used = not self.is_normalize_used

    def is_normalization_used(self):
        return self.is_normalize_used
