import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog)

from apen import ApEn, makeReport


class ApEnWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        mLabel = QLabel('m')
        self.mEdit = QLineEdit("2")

        nLabel = QLabel('Minumum size')
        nEdit = QLineEdit('30')

        fileNamesLabel = QLabel("Files to analyze")
        self.fileNamesEdit = QTextEdit()
        fileNamesOpen = QPushButton("Open files",self)
        fileNamesOpen.clicked.connect(self.showFileChooser)

        apEnCalculate = QPushButton("Calculate ApEn",self)
        apEnCalculate.clicked.connect(self.calculateApEn)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(mLabel, 1, 0)
        grid.addWidget(self.mEdit, 1, 1)

        grid.addWidget(fileNamesLabel, 2, 0)
        grid.addWidget(self.fileNamesEdit, 2, 1)
        grid.addWidget(fileNamesOpen, 2, 2)

        grid.addWidget(apEnCalculate, 3, 1, 3, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()

    def calculateApEn(self):
        results = []
        tmp = None
        r = []
        filesList = self.fileNamesEdit.toPlainText().split('\n')
        for i in filesList:
            try:
                m=int(self.mEdit.text())
                tmp = ApEn(m=m)
                res = tmp.prepare_calculate_apen(m=m,series=i)
                results.append('{0:.10f}'.format(res))
                r.append(tmp.r)
            except ValueError:
                results.append("Error!")
        makeReport(filesList=filesList,apEnList=results,rList=r)

    def showFileChooser(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file', '/home', ("DAT (*.dat, *.txt)"))
        self.fileNamesEdit.setText("")
        print(fname)
        for name in fname[0]:
            self.fileNamesEdit.append(name)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ApEnWidget()
    sys.exit(app.exec_())