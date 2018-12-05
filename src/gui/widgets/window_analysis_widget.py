from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout


class WindowAnalysisWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        window_size_label = QLabel("window width")
        self.window_size = QLineEdit("100")

        window_step_label = QLabel("window step")
        self.window_step = QLineEdit("10")

        grid = QGridLayout()
        grid.addWidget(window_size_label, 0, 0)
        grid.addWidget(self.window_size, 0, 1)
        grid.addWidget(window_step_label, 1, 0)
        grid.addWidget(self.window_step, 1, 1)

        self.setLayout(grid)

    def get_window_size(self):
        res = -1
        try:
            res = float(self.window_size.text())
        except:
            pass
        return res

    def get_window_step(self):
        res = -1
        try:
            res = float(self.window_step.text())
        except:
            pass
        return res
