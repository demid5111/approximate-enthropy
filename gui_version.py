import os
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QRadioButton, QButtonGroup,
                             QHBoxLayout, QCheckBox, QBoxLayout, QVBoxLayout, QMessageBox)

from apen import ApEn, makeReport
from supporting import CalculationType


class ApEnWidget(QWidget):
    def __init__(self):
        super().__init__()
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

        apEnCalculate = QPushButton("Calculate ApEn", self)
        apEnCalculate.clicked.connect(self.calculateApEn)

        grid = QGridLayout()
        self.setLayout(grid)
        # self.layout().setSpacing(10)

        grid.addWidget(mLabel,0,0)
        grid.addWidget(self.mEdit,0,1)

        grid.addWidget(cb, 1, 0)
        grid.addWidget(self.rThreshold, 1, 1)

        grid.addWidget(rLabel, 2, 0)
        grid.addLayout(number_group, 2, 1)

        grid.addWidget(fileNamesLabel, 3, 0)
        grid.addWidget(self.fileNamesEdit, 3, 1)
        grid.addWidget(fileNamesOpen, 3, 2)


        grid.addWidget(apEnCalculate, 4, 1, 3, 1)

        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()


    def calculateApEn(self):
        results = []
        tmp = None
        r = []
        filesList = self.fileNamesEdit.toPlainText().split('\n')
        # 1. decide whether to use threshold or not
        thresholdValue = -1
        devCoefValue = -1
        if self.isThresholdUsed:
            thresholdValue = self.rThreshold.text()
        # 2. choose the way to calculate r
        if self.calculateR == CalculationType.DEV:
            devCoefValue = self.rDevCoef.text()
        # 3. make all enthropy calculations
        for i in filesList:
            try:
                m = int(self.mEdit.text())
                tmp = ApEn(m=m)
                thresholdValue = int(thresholdValue)
                devCoefValue = float(devCoefValue)
                res = tmp.prepare_calculate_apen(m=m,
                                                          series=i,
                                                          calculationType=self.calculateR,
                                                          devCoefValue=devCoefValue,
                                                          useThreshold=self.isThresholdUsed,
                                                          thresholdValue=thresholdValue)
                results.append('{0:.10f}'.format(res))
                r.append(tmp.r)
                dialog =  QMessageBox(self)
                dialog.setWindowModality(False)
                dialog.setText("ApEn calculated for " + i)
                # information(self,"ApEn","ApEn calculated for " + i);
                # dialog.setText("MESSAGE")
                dialog.show()
            except ValueError:
                results.append("Error!")
        makeReport(filesList=filesList, apEnList=results, rList=r)


    def showFileChooser(self):
        path = ""
        try:
            with open (self.fileName,"r") as f:
                path = f.readline().strip()
        except FileNotFoundError:
            pass
        fname = QFileDialog.getOpenFileNames(self,  'Open file', path, ("DAT (*.dat, *.txt)"))
        self.fileNamesEdit.setText("")
        print(fname)
        for name in fname[0]:
            self.fileNamesEdit.append(name)
        self.memorizeLastPath()

    def memorizeLastPath(self):
        if not self.fileNamesEdit:
            return
        path = os.path.dirname(self.fileNamesEdit.toPlainText().split('\n')[0])
        with open(self.fileName,"w") as f:
            f.write(path+'/')

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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ApEnWidget()
    sys.exit(app.exec_())
