from PyQt5.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QHBoxLayout, QLineEdit, QCheckBox, QLabel, QGridLayout

from src.utils.supporting import CalculationType


class EntropyWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.init_ui()

    def config_r_enth_group(self):
        number_group = QVBoxLayout()  # Number group
        self.calculateR = CalculationType.CONST
        self.rConst = QRadioButton("r=0.2*SDNN")
        self.rConst.setChecked(True)
        self.rConst.clicked.connect(self.set_const_r)
        number_group.addWidget(self.rConst)
        # self.rDev = QRadioButton("r=Rmax")

        dev_coef_group = QHBoxLayout()
        self.rDev = QRadioButton('r = SDNN * ', self)
        self.rDev.clicked.connect(self.set_dev_r)
        self.rDevCoef = QLineEdit("0.5")
        self.rDevCoef.setEnabled(False)
        dev_coef_group.addWidget(self.rDev)
        dev_coef_group.addWidget(self.rDevCoef)
        number_group.addLayout(dev_coef_group)

        self.rComplex = QRadioButton("r=Rchon")
        self.rComplex.clicked.connect(self.set_complex_r)
        number_group.addWidget(self.rComplex)

        return number_group

    def init_ui(self):
        cb = QCheckBox('Use threshold', self)
        cb.setChecked(True)
        self.is_threshold_used = True
        cb.clicked.connect(self.toggle_threshold_checkbox)
        self.rThreshold = QLineEdit("300")

        window_cb = QCheckBox('Use windows', self)
        window_cb.setChecked(True)
        window_cb.clicked.connect(self.toggle_window_checkbox)
        self.window_size_edit = QLineEdit("100")
        self.window_step_edit = QLineEdit("10")
        self.is_windows_enabled = True

        rLabel = QLabel("r")
        number_group = self.config_r_enth_group()

        grid = QGridLayout()
        grid.addWidget(cb, 0, 0)
        grid.addWidget(self.rThreshold, 0, 1)
        grid.addWidget(window_cb, 1, 0)
        grid.addWidget(self.window_size_edit, 1, 1)
        grid.addWidget(self.window_step_edit, 2, 1)
        grid.addWidget(rLabel, 3, 0)
        grid.addLayout(number_group, 3, 1)
        self.setLayout(grid)

    def set_complex_r(self):
        self.calculateR = CalculationType.COMPLEX
        self.rDevCoef.setEnabled(False)

    def set_const_r(self):
        self.calculateR = CalculationType.CONST
        self.rDevCoef.setEnabled(False)

    def set_dev_r(self):
        self.calculateR = CalculationType.DEV
        self.rDevCoef.setEnabled(True)

    def toggle_threshold_checkbox(self):
        self.is_threshold_used = not self.is_threshold_used
        self.rThreshold.setEnabled(self.is_threshold_used)

    def toggle_window_checkbox(self):
        self.is_windows_enabled = not self.is_windows_enabled
        self.window_size_edit.setEnabled(self.is_windows_enabled)
        self.window_step_edit.setEnabled(self.is_windows_enabled)
