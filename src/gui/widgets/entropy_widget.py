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

        dev_coef_group = QHBoxLayout()
        self.rDev = QRadioButton('r = SDNN * ', self)
        self.rDev.clicked.connect(self.set_dev_r)
        self.rDevCoef = QLineEdit("0.5")
        self.rDevCoef.setEnabled(False)
        self.rDevCoef.setFixedWidth(40)
        dev_coef_group.addWidget(self.rDev)
        dev_coef_group.addWidget(self.rDevCoef)
        number_group.addLayout(dev_coef_group)

        self.rComplex = QRadioButton("r=Rchon")
        self.rComplex.clicked.connect(self.set_complex_r)
        number_group.addWidget(self.rComplex)

        return number_group

    def init_ui(self):
        self.ap_en_cb = QCheckBox('Calculate Approximate Entropy', self)
        self.is_ap_en_used = True
        self.ap_en_cb.setChecked(self.is_ap_en_used)
        self.ap_en_cb.clicked.connect(self.toggle_ap_en_cb)

        self.samp_en_cb = QCheckBox('Calculate Sample Entropy', self)
        self.is_samp_en_used = True
        self.samp_en_cb.setChecked(self.is_samp_en_used)
        self.samp_en_cb.clicked.connect(self.toggle_samp_en_cb)

        self.threshold_cb = QCheckBox('Check for threshold', self)
        self.is_threshold_used = True
        self.threshold_cb.setChecked(self.is_threshold_used)
        self.threshold_cb.clicked.connect(self.toggle_threshold_checkbox)

        descr = 'threshold (minumum number<br>of elements in a sequence)'
        self.r_threshold_label = QLabel('<p style="text-align:right">{}</p>'.format(descr))
        self.r_threshold = QLineEdit("300")

        rLabel = QLabel("r (maximum distance between<br>vectors that can be considered<br> as close to each other)")
        number_group = self.config_r_enth_group()

        grid = QGridLayout()
        grid.addWidget(self.threshold_cb, 0, 0, 1, 2)
        grid.addWidget(self.r_threshold_label, 1, 0)
        grid.addWidget(self.r_threshold, 1, 1)

        grid.addWidget(rLabel, 3, 0)
        grid.addLayout(number_group, 3, 1)
        grid.addWidget(self.ap_en_cb, 4, 0)
        grid.addWidget(self.samp_en_cb, 5, 0)

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
        self.r_threshold.setEnabled(self.is_threshold_used)

    def toggle_ap_en_cb(self):
        self.is_ap_en_used = not self.is_ap_en_used
        self.ap_en_cb.setChecked(self.is_ap_en_used)

    def toggle_samp_en_cb(self):
        self.is_samp_en_used = not self.is_samp_en_used
        self.samp_en_cb.setChecked(self.is_samp_en_used)

    def is_samp_en(self):
        return self.is_samp_en_used

    def is_ap_en(self):
        return self.is_ap_en_used

    def set_samp_en(self, v):
        self.is_samp_en_used = v
        self.samp_en_cb.setChecked(self.is_samp_en_used)

    def set_ap_en(self, v):
        self.is_ap_en_used = v
        self.ap_en_cb.setChecked(self.is_ap_en_used)

    def get_threshold(self):
        return int(self.r_threshold.text()) if self.is_threshold_used else -1

    def get_dev_coef_value(self):
        return float(self.rDevCoef.text()) if self.calculateR == CalculationType.DEV else -1

    def get_calculation_type(self):
        return self.calculateR

    def is_threshold(self):
        return self.is_threshold_used

    def reset_to_default(self):
        self.set_ap_en(True)
        self.set_samp_en(True)
        self.r_threshold.setText('300')
        self.r_threshold.setEnabled(True)
        self.threshold_cb.setChecked(True)
