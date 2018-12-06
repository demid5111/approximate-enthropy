import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from src.gui.widgets.ap_en_widget import ApEnWidget


class App(QMainWindow):
    def __init__(self, isShown=True):
        super().__init__()
        self.title = 'HeartAlgo-Analyzer'
        self.left = 400
        self.top = 100
        self.width = 500
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = ApEnWidget(self)
        self.setCentralWidget(self.table_widget)
        self.resize(self.width, self.height)
        if isShown:
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())
