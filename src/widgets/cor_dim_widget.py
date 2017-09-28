from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout


class CorDimWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        cor_dim_radius_label = QLabel("radius")
        self.cor_dim_radius = QLineEdit("0.99")

        grid = QGridLayout()
        grid.addWidget(cor_dim_radius_label, 0, 0)
        grid.addWidget(self.cor_dim_radius, 0, 1)

        self.setLayout(grid)

    def get_radius(self):
        res = -1
        try:
            res = float(self.cor_dim_radius.text())
        except:
            pass
        return res
