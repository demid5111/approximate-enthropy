from PyQt5.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QHBoxLayout, QLineEdit, QCheckBox, QLabel, QGridLayout

from src.utils.supporting import CalculationType


class PertropyWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.normalize_cb = QCheckBox('Normalize by (n-1)', self)
        self.is_normalize_used = True
        self.normalize_cb.setChecked(self.is_normalize_used)
        self.normalize_cb.clicked.connect(self.toggle_normalize_cb)

        self.strides_cb = QCheckBox('Use strides', self)
        self.is_stride_used = True
        self.strides_cb.setChecked(self.is_stride_used)
        # cb.clicked.connect(self.toggle_stride_checkbox)

        descr = 'stride (or step, "1" means<br>one after another)'
        self.stride_label = QLabel('<p style="text-align:right">{}</p>'.format(descr))
        self.stride_value = QLineEdit("2")

        grid = QGridLayout()
        grid.addWidget(self.normalize_cb, 0, 0, 1, 3)
        grid.addWidget(self.strides_cb, 1, 0)
        grid.addWidget(self.stride_label, 2, 1)
        grid.addWidget(self.stride_value, 2, 2)


        self.setLayout(grid)

    def toggle_normalize_cb(self):
        self.is_normalize_used = not self.is_normalize_used

    def is_normalization_used(self):
        return self.is_normalize_used
