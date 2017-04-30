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
        #
        cb = QCheckBox('Use threshold', self)
        cb.setChecked(True)
        cb.clicked.connect(self.toogleThresholdCheckbox)
        self.rThreshold = QLineEdit("300")
        self.isThresholdUsed = True

        self.calculateR = CalculationType.CONST
        self.rConst = QRadioButton("r=0.2*SDNN")
        self.rConst.setChecked(True)
        self.rConst.clicked.connect(self.setConstR)
        number_group.addWidget(self.rConst)
        # self.rDev = QRadioButton("r=Rmax")

        devCoefGroup = QHBoxLayout()

        self.rDev = QRadioButton('r = SDNN * ', self)
        self.rDev.clicked.connect(self.setDevR)
        self.rDevCoef = QLineEdit("0.5")
        self.rDevCoef.setEnabled(False)
        devCoefGroup.addWidget(self.rDev)
        devCoefGroup.addWidget(self.rDevCoef)
        number_group.addLayout(devCoefGroup)

        self.rComplex = QRadioButton("r=Rchon")
        self.rComplex.clicked.connect(self.setComplexR)
        number_group.addWidget(self.rComplex)

        fileNamesLabel = QLabel("Files to analyze")
        self.fileNamesEdit = QTextEdit()
        fileNamesOpen = QPushButton("Open files", self)
        fileNamesOpen.clicked.connect(self.showFileChooser)

        fileNamesClean = QPushButton("Clean files", self)
        fileNamesClean.clicked.connect(self.cleanFileNames)

        apEnCalculate = QPushButton("Calculate ApEn", self)
        apEnCalculate.clicked.connect(self.calculate_apen)

        # self.move(300, 150)
        # self.setWindowTitle('Calculator')
        # self.show()

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        # self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Enthropy")
        # self.tabs.addTab(self.tab2, "SampEn")

        # Create first tab

        grid = QGridLayout()
        self.tab1.layout = grid
        #
        grid.addWidget(mLabel, 0, 0)
        grid.addWidget(self.mEdit, 0, 1)

        grid.addWidget(cb, 1, 0)
        grid.addWidget(self.rThreshold, 1, 1)

        grid.addWidget(rLabel, 2, 0)
        grid.addLayout(number_group, 2, 1)

        grid.addWidget(fileNamesLabel, 3, 0)
        grid.addWidget(self.fileNamesEdit, 3, 1)

        fileButtonsGroup = QVBoxLayout()
        fileButtonsGroup.addWidget(fileNamesOpen)
        fileButtonsGroup.addWidget(fileNamesClean)

        grid.addLayout(fileButtonsGroup, 3, 2)
        # grid.addWidget(fileNamesOpen, 3, 2)
        # grid.addWidget(fileNamesClean, 3, 3)

        grid.addWidget(apEnCalculate, 4, 1, 3, 1)

        self.tab1.setLayout(self.tab1.layout)

        sampEnCalculate = QPushButton("Calculate SampEn", self)
        sampEnCalculate.clicked.connect(self.sampEnCalculate)

        grid.addWidget(sampEnCalculate, 7, 1, 3, 1)
        # self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def cleanFileNames(self):
        self.fileNamesEdit.clear()

    def sampEnCalculate(self):
        results = []
        r = []
        n = []
        avg_rr = []
        files_list = self.fileNamesEdit.toPlainText().split('\n')
        # 1. decide whether to use threshold or not
        thresholdValue = -1
        devCoefValue = -1
        if self.isThresholdUsed:
            thresholdValue = self.rThreshold.text()
        # 2. choose the way to calculate r
        if self.calculateR == CalculationType.DEV:
            devCoefValue = self.rDevCoef.text()
        # 3. make all enthropy calculations
        files_success = []
        tmp = SampEn()
        for file_name in files_list:
            try:
                res = tmp.prepare_calculate_sampen(m=int(self.mEdit.text()),
                                                   series=file_name,
                                                   calculation_type=self.calculateR,
                                                   dev_coef_value=float(devCoefValue),
                                                   use_threshold=self.isThresholdUsed,
                                                   threshold_value=int(thresholdValue))
                results.append('{0:.10f}'.format(tmp.get_result_val(res)))
                files_success.append(file_name)
                r.append(tmp.get_r_val(res))
                n.append(tmp.get_n_val(res))
                avg_rr.append(tmp.get_avg_rr_val(res))
            except ValueError:
                results.append("Error! For file {}".format(file_name))
        dialog = QMessageBox(self)
        dialog.setWindowModality(False)
        dialog.setText("SampEn calculated for: \n {}"
                       .format("".join(["- {}, \n".format(i) for i in files_success])))
        dialog.show()
        make_report(files_list=files_list, ap_en_list=results, r_list=r, n_list=n, avg_rr_list=avg_rr, is_ap_en=False)

    def calculate_apen(self):
        results = []
        r = []
        n = []
        avg_rr = []
        files_list = self.fileNamesEdit.toPlainText().split('\n')
        # 1. decide whether to use threshold or not
        thresholdValue = -1
        devCoefValue = -1
        if self.isThresholdUsed:
            thresholdValue = self.rThreshold.text()
        # 2. choose the way to calculate r
        if self.calculateR == CalculationType.DEV:
            devCoefValue = self.rDevCoef.text()
        # 3. make all enthropy calculations
        files_success = []
        tmp = ApEn()
        for file_name in files_list:
            try:
                res = tmp.prepare_calculate_apen(m=int(self.mEdit.text()),
                                                 file_name=file_name,
                                                 calculation_type=self.calculateR,
                                                 dev_coef_value=float(devCoefValue),
                                                 use_threshold=self.isThresholdUsed,
                                                 threshold_value=int(thresholdValue))
                results.append('{0:.10f}'.format(tmp.get_result_val(res)))
                files_success.append(file_name)
                r.append(tmp.get_r_val(res))
                n.append(tmp.get_n_val(res))
                avg_rr.append(tmp.get_avg_rr_val(res))
            except ValueError:
                results.append("Error! For file {}".format(file_name))
        dialog = QMessageBox(self)
        dialog.setWindowModality(False)
        dialog.setText("ApEn calculated for: \n {}"
                       .format("".join(["- {}, \n".format(i) for i in files_success])))
        dialog.show()
        make_report(files_list=files_list, ap_en_list=results, r_list=r, n_list=n, avg_rr_list=avg_rr, is_ap_en=True)

    def showFileChooser(self):
        path = ""
        try:
            with open(self.fileName, "r") as f:
                path = f.readline().strip()
        except FileNotFoundError:
            pass
        fname = QFileDialog.getOpenFileNames(self, 'Open file', path, ("DAT (*.dat, *.txt)"))
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

    def toogleThresholdCheckbox(self):
        self.isThresholdUsed = not self.isThresholdUsed
        self.rThreshold.setEnabled(self.isThresholdUsed)

    def setComplexR(self):
        self.calculateR = CalculationType.COMPLEX
        self.rDevCoef.setEnabled(False)

    def setConstR(self):
        self.calculateR = CalculationType.CONST
        self.rDevCoef.setEnabled(False)

    def setDevR(self):
        self.calculateR = CalculationType.DEV
        self.rDevCoef.setEnabled(True)


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
