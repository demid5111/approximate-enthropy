import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from src.widgets.ap_en_widget import ApEnWidget


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'HeartAlgo-Analyzer'
        self.left = 400
        self.top = 200
        self.width = 400
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = ApEnWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
