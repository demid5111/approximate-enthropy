import os
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QRadioButton, QButtonGroup,
                             QHBoxLayout, QCheckBox, QBoxLayout, QVBoxLayout, QMessageBox, QMainWindow, QTabWidget)

from apen import ApEn, make_report
from sampen import SampEn
from supporting import CalculationType


class ApEnWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.fileName = ".memory"
        self.initUI()

    def initUI(self):
        mLabel = QLabel('m')
        self.mEdit = QLineEdit("2")

        rLabel = QLabel("r")
        number_group = QVBoxLayout()  # Number group

        cb = QCheckBox('Use threshold', self)
        cb.setChecked(True)
        cb.clicked.connect(self.toggle_threshold_checkbox)
        self.rThreshold = QLineEdit("300")
        self.is_threshold_used = True

        window_cb = QCheckBox('Use windows', self)
        window_cb.setChecked(True)
        window_cb.clicked.connect(self.toggle_window_checkbox)
        self.window_size_edit = QLineEdit("100")
        self.window_step_edit = QLineEdit("10")
        self.is_windows_enabled = True

        self.calculateR = CalculationType.CONST
        self.rConst = QRadioButton("r=0.2*SDNN")
        self.rConst.setChecked(True)
        self.rConst.clicked.connect(self.setConstR)
        number_group.addWidget(self.rConst)
        # self.rDev = QRadioButton("r=Rmax")

        dev_coef_group = QHBoxLayout()
        self.rDev = QRadioButton('r = SDNN * ', self)
        self.rDev.clicked.connect(self.setDevR)
        self.rDevCoef = QLineEdit("0.5")
        self.rDevCoef.setEnabled(False)
        dev_coef_group.addWidget(self.rDev)
        dev_coef_group.addWidget(self.rDevCoef)
        number_group.addLayout(dev_coef_group)

        self.rComplex = QRadioButton("r=Rchon")
        self.rComplex.clicked.connect(self.setComplexR)
        number_group.addWidget(self.rComplex)

        fileNamesLabel = QLabel("Files to analyze")
        self.fileNamesEdit = QTextEdit()
        fileNamesOpen = QPushButton("Open files", self)
        fileNamesOpen.clicked.connect(self.showFileChooser)

        fileNamesClean = QPushButton("Clean files", self)
        fileNamesClean.clicked.connect(self.clean_file_names)

        apEnCalculate = QPushButton("Calculate ApEn", self)
        apEnCalculate.clicked.connect(self.calculate_apen)

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        # self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Entropy")

        # Create first tab

        grid = QGridLayout()
        self.tab1.layout = grid
        #
        grid.addWidget(mLabel, 0, 0)
        grid.addWidget(self.mEdit, 0, 1)

        grid.addWidget(cb, 1, 0)
        grid.addWidget(self.rThreshold, 1, 1)

        grid.addWidget(window_cb, 2, 0)
        grid.addWidget(self.window_size_edit, 2, 1)
        grid.addWidget(self.window_step_edit, 3, 1)

        grid.addWidget(rLabel, 4, 0)
        grid.addLayout(number_group, 4, 1)

        grid.addWidget(fileNamesLabel, 5, 0)
        grid.addWidget(self.fileNamesEdit, 5, 1)

        file_buttons_group = QVBoxLayout()
        file_buttons_group.addWidget(fileNamesOpen)
        file_buttons_group.addWidget(fileNamesClean)

        grid.addLayout(file_buttons_group, 5, 2)

        grid.addWidget(apEnCalculate, 6, 1, 3, 1)

        self.tab1.setLayout(self.tab1.layout)

        samp_en_calculate = QPushButton("Calculate SampEn", self)
        samp_en_calculate.clicked.connect(self.calculate_sampen)

        grid.addWidget(samp_en_calculate, 9, 1, 3, 1)
        # self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def clean_file_names(self):
        self.fileNamesEdit.clear()

    def calculate_sampen(self):
        files_list, threshold_value, dev_coef_value, window_size, step_size = self.get_parameters()
        res_dic = {}
        tmp = SampEn()
        for file_name in files_list:
            try:
                res = tmp.prepare_calculate_window_sampen(m=int(self.mEdit.text()),
                                                          file_name=file_name,
                                                          calculation_type=self.calculateR,
                                                          dev_coef_value=dev_coef_value,
                                                          use_threshold=self.is_threshold_used,
                                                          threshold_value=threshold_value,
                                                          window_size=window_size,
                                                          step_size=step_size)
                res_dic[file_name] = res
            except ValueError:
                res_dic[file_name] = {'error': "Error! For file {}".format(file_name)}
        dialog = QMessageBox(self)
        dialog.setWindowModality(False)
        dialog.setText("SampEn calculated for: \n {}".format("".join(["- {}, \n".format(i) for i in res_dic.keys()])))
        dialog.show()
        make_report(res_dic=res_dic, is_ap_en=False)

    def calculate_apen(self):
        files_list, threshold_value, dev_coef_value, window_size, step_size = self.get_parameters()
        res_dic = {}
        tmp = ApEn()
        for file_name in files_list:
            try:
                res = tmp.prepare_calculate_window_apen(m=int(self.mEdit.text()),
                                                        file_name=file_name,
                                                        calculation_type=self.calculateR,
                                                        dev_coef_value=dev_coef_value,
                                                        use_threshold=self.is_threshold_used,
                                                        threshold_value=threshold_value,
                                                        window_size=window_size,
                                                        step_size=step_size)
                res_dic[file_name] = res
            except ValueError:
                res_dic[file_name] = {'error': "Error! For file {}".format(file_name)}
        dialog = QMessageBox(self)
        dialog.setWindowModality(False)
        dialog.setText("ApEn calculated for: \n {}".format("".join(["- {}, \n".format(i) for i in res_dic.keys()])))
        dialog.show()
        make_report(res_dic=res_dic, is_ap_en=True)

    def showFileChooser(self):
        path = ""
        try:
            with open(self.fileName, "r") as f:
                path = f.readline().strip()
        except FileNotFoundError:
            pass
        fname = QFileDialog.getOpenFileNames(self, 'Open file', path, "DAT (*.dat, *.txt)")
        self.fileNamesEdit.setText("")
        print(fname)
        for name in fname[0]:
            self.fileNamesEdit.append(name)
        self.memorizeLastPath()

    def memorizeLastPath(self):
        if not self.fileNamesEdit:
            return
        path = os.path.dirname(self.fileNamesEdit.toPlainText().split('\n')[0])
        with open(self.fileName, "w") as f:
            f.write(path + '/')

    def toggle_threshold_checkbox(self):
        self.is_threshold_used = not self.is_threshold_used
        self.rThreshold.setEnabled(self.is_threshold_used)

    def toggle_window_checkbox(self):
        self.is_windows_enabled = not self.is_windows_enabled
        self.window_size_edit.setEnabled(self.is_windows_enabled)
        self.window_step_edit.setEnabled(self.is_windows_enabled)

    def setComplexR(self):
        self.calculateR = CalculationType.COMPLEX
        self.rDevCoef.setEnabled(False)

    def setConstR(self):
        self.calculateR = CalculationType.CONST
        self.rDevCoef.setEnabled(False)

    def setDevR(self):
        self.calculateR = CalculationType.DEV
        self.rDevCoef.setEnabled(True)

    def get_parameters(self):
        files_list = self.fileNamesEdit.toPlainText().split('\n')
        threshold_value = int(self.rThreshold.text()) if self.is_threshold_used else -1
        dev_coef_value = float(self.rDevCoef.text()) if self.calculateR == CalculationType.DEV else -1
        window_size = int(self.window_size_edit.text()) if self.is_windows_enabled else 0
        step_size = int(self.window_step_edit.text()) if self.is_windows_enabled else 0
        return files_list, threshold_value, dev_coef_value, window_size, step_size


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'HeartAlgo-Analyzer'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = ApEnWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
