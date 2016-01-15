import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog)


class ApEnWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        mLabel = QLabel('m')
        mEdit = QLineEdit()

        nLabel = QLabel('Minumum size')
        nEdit = QLineEdit('30')

        fileNamesLabel = QLabel("Files to analyze")
        self.fileNamesEdit = QTextEdit()
        fileNamesOpen = QPushButton("Open files",self)
        fileNamesOpen.clicked.connect(self.showFileChooser)

        apEnCalculate = QPushButton("Calculate ApEn",self)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(mLabel, 1, 0)
        grid.addWidget(mEdit, 1, 1)

        grid.addWidget(fileNamesLabel, 2, 0)
        grid.addWidget(self.fileNamesEdit, 2, 1)
        grid.addWidget(fileNamesOpen, 2, 2)

        grid.addWidget(apEnCalculate, 3, 1, 3, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()

    def showFileChooser(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file', '/home', ("DAT (*.dat)"))
        self.fileNamesEdit.setText("")
        print(fname)
        for name in fname[0]:
            self.fileNamesEdit.append(name)





if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ApEnWidget()
    sys.exit(app.exec_())