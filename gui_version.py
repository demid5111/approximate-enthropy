import os
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QRadioButton,
                             QHBoxLayout, QCheckBox, QVBoxLayout, QMessageBox, QMainWindow, QTabWidget)

from apen import ApEn, make_report
from cordim import CorDim
from sampen import SampEn
from supporting import CalculationType


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
        # self.rDev = QRadioButton("r=Rmax")

        dev_coef_group = QHBoxLayout()
        self.rDev = QRadioButton('r = SDNN * ', self)
        self.rDev.clicked.connect(self.set_dev_r)
        self.rDevCoef = QLineEdit("0.5")
        self.rDevCoef.setEnabled(False)
        dev_coef_group.addWidget(self.rDev)
        dev_coef_group.addWidget(self.rDevCoef)
        number_group.addLayout(dev_coef_group)

        self.rComplex = QRadioButton("r=Rchon")
        self.rComplex.clicked.connect(self.set_complex_r)
        number_group.addWidget(self.rComplex)

        return number_group

    def init_ui(self):
        cb = QCheckBox('Use threshold', self)
        cb.setChecked(True)
        self.is_threshold_used = True
        cb.clicked.connect(self.toggle_threshold_checkbox)
        self.rThreshold = QLineEdit("300")

        window_cb = QCheckBox('Use windows', self)
        window_cb.setChecked(True)
        window_cb.clicked.connect(self.toggle_window_checkbox)
        self.window_size_edit = QLineEdit("100")
        self.window_step_edit = QLineEdit("10")
        self.is_windows_enabled = True

        rLabel = QLabel("r")
        number_group = self.config_r_enth_group()

        grid = QGridLayout()
        grid.addWidget(cb, 0, 0)
        grid.addWidget(self.rThreshold, 0, 1)
        grid.addWidget(window_cb, 1, 0)
        grid.addWidget(self.window_size_edit, 1, 1)
        grid.addWidget(self.window_step_edit, 2, 1)
        grid.addWidget(rLabel, 3, 0)
        grid.addLayout(number_group, 3, 1)
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
        self.rThreshold.setEnabled(self.is_threshold_used)

    def toggle_window_checkbox(self):
        self.is_windows_enabled = not self.is_windows_enabled
        self.window_size_edit.setEnabled(self.is_windows_enabled)
        self.window_step_edit.setEnabled(self.is_windows_enabled)


class CorDimWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        cor_dim_radius_label = QLabel("radius")
        self.cor_dim_radius = QLineEdit("0.99")

        # cor_dim_calculate = QPushButton("Calculate CorDim", self)
        # cor_dim_calculate.clicked.connect(self.calculate_cor_dim)

        grid = QGridLayout()
        grid.addWidget(cor_dim_radius_label, 0, 0)
        grid.addWidget(self.cor_dim_radius, 0, 1)
        # grid.addWidget(cor_dim_calculate, 1, 1, 3, 1)

        self.setLayout(grid)


class ApEnWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.fileName = ".memory"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(500, 600)

        # Add tabs
        self.tabs.addTab(self.tab1, "Entropy")
        # self.tabs.addTab(self.tab2, "CorDim")

        # Create first tab
        enth_grid = self.config_entropy_tab()

        self.tab1.setLayout(enth_grid)
        # self.tab2.setLayout(cor_dim_grid)

        # Add tabs to widget
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def config_filechooser_group(self):
        fileNamesOpen = QPushButton("Open files", self)
        fileNamesOpen.clicked.connect(self.show_file_chooser)

        fileNamesClean = QPushButton("Clean files", self)
        fileNamesClean.clicked.connect(self.clean_file_names)

        file_chooser_group = QGridLayout()
        fileNamesLabel = QLabel("Files to analyze")
        self.fileNamesEdit = QTextEdit()

        file_buttons_group = QVBoxLayout()
        file_buttons_group.addWidget(fileNamesOpen)
        file_buttons_group.addWidget(fileNamesClean)

        file_chooser_group.addWidget(fileNamesLabel, 0, 0)
        file_chooser_group.addWidget(self.fileNamesEdit, 0, 1)
        file_chooser_group.addLayout(file_buttons_group, 0, 2)

        return file_chooser_group

    def config_ent_settings_grid(self):
        cb = QCheckBox('Use threshold', self)
        cb.setChecked(True)
        self.is_threshold_used = True
        cb.clicked.connect(self.toggle_threshold_checkbox)
        self.rThreshold = QLineEdit("300")

        window_cb = QCheckBox('Use windows', self)
        window_cb.setChecked(True)
        window_cb.clicked.connect(self.toggle_window_checkbox)
        self.window_size_edit = QLineEdit("100")
        self.window_step_edit = QLineEdit("10")
        self.is_windows_enabled = True

        rLabel = QLabel("r")
        # number_group = self.config_r_enth_group()

        grid = QGridLayout()
        grid.addWidget(cb, 0, 0)
        grid.addWidget(self.rThreshold, 0, 1)
        grid.addWidget(window_cb, 1, 0)
        grid.addWidget(self.window_size_edit, 1, 1)
        grid.addWidget(self.window_step_edit, 2, 1)
        grid.addWidget(rLabel, 3, 0)
        # grid.addLayout(number_group, 3, 1)

        return grid

    def config_entropy_tab(self):
        mLabel = QLabel('m')
        self.mEdit = QLineEdit("2")

        self.is_use_ent_cb = QCheckBox('Calculate entropy?', self)
        self.is_use_ent_cb.setChecked(True)
        self.is_calc_ent = True
        self.is_use_ent_cb.clicked.connect(self.toggle_calc_ent_cb)

        self.ent_widget = EntropyWidget(self)

        self.is_use_cor_dim_cb = QCheckBox('Calculate cor dim?', self)
        self.is_use_cor_dim_cb.setChecked(True)
        self.is_calc_cor_dim = True
        self.is_use_cor_dim_cb.clicked.connect(self.toggle_calc_cor_dim_cb)

        self.cor_dim_widget = CorDimWidget(self)

        self.run_calculate = QPushButton("Run calculation", self)
        self.run_calculate.clicked.connect(self.calculate)

        # samp_en_calculate = QPushButton("Calculate SampEn", self)
        # samp_en_calculate.clicked.connect(self.calculate_sampen)

        grid = QGridLayout()
        grid.addWidget(mLabel, 0, 0)
        grid.addWidget(self.mEdit, 0, 1)
        grid.addWidget(self.is_use_ent_cb, 1, 1)
        grid.addWidget(self.ent_widget, 2, 1)
        grid.addWidget(self.is_use_cor_dim_cb, 3, 1)
        grid.addWidget(self.cor_dim_widget, 4, 1)
        # grid.addLayout(file_chooser_group, 5, 0, 1, 3)  # spanning it over 3 columns, keeping one row
        grid.addWidget(self.run_calculate, 8, 1, 3, 1)
        # grid.addWidget(samp_en_calculate, 10, 1, 3, 1)

        # cor_dim_grid = self.config_cordim_grid()
        file_chooser_group = self.config_filechooser_group()

        grid.addLayout(file_chooser_group, 5, 0, 1, 3)
        # grid.addLayout(cor_dim_grid, 15, 0, 1, 3)

        return grid

    def config_cordim_grid(self):
        cor_dim_radius_label = QLabel("radius")
        self.cor_dim_radius = QLineEdit("0.99")

        cor_dim_calculate = QPushButton("Calculate CorDim", self)
        cor_dim_calculate.clicked.connect(self.calculate_cor_dim)

        grid = QGridLayout()
        grid.addWidget(cor_dim_radius_label, 0, 0)
        grid.addWidget(self.cor_dim_radius, 0, 1)
        grid.addWidget(cor_dim_calculate, 1, 1, 3, 1)

        return grid

    def clean_file_names(self):
        self.fileNamesEdit.clear()

    def calculate(self):
        pass

    def calculate_sampen(self):
        files_list, threshold_value, dev_coef_value, window_size, step_size = self.get_entropy_parameters()
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

        self.show_message('SampEn', res_dic)
        make_report(res_dic=res_dic, is_ap_en=False)

    def calculate_apen(self):
        files_list, threshold_value, dev_coef_value, window_size, step_size = self.get_entropy_parameters()
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
        self.show_message('ApEn', res_dic)
        make_report(res_dic=res_dic, is_ap_en=True)

    def calculate_cor_dim(self):
        files_list, dimension, radius = self.get_cor_dim_parameters()
        res_dic = {}
        tmp = CorDim()
        for file_name in files_list:
            try:
                res = tmp.calculate_cor_dim(file_name=file_name,
                                            dimension=dimension,
                                            radius=radius)
                res_dic[file_name] = res
            except ValueError:
                res_dic[file_name] = {'error': "Error! For file {}".format(file_name)}
        self.show_message('CorDim', res_dic)
        make_report(res_dic=res_dic, is_ap_en=True)

    def show_message(self, source, res_dic):
        dialog = QMessageBox(self)
        dialog.setWindowModality(False)
        dialog.setText(
                "{} calculated for: \n {}".format(source, "".join(["- {}, \n".format(i) for i in res_dic.keys()])))
        dialog.show()

    def show_file_chooser(self):
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
        self.memorize_last_path()

    def memorize_last_path(self):
        if not self.fileNamesEdit:
            return
        path = os.path.dirname(self.fileNamesEdit.toPlainText().split('\n')[0])
        with open(self.fileName, "w") as f:
            f.write(path + '/')

    def toggle_calc_ent_cb(self):
        self.is_calc_ent = not self.is_calc_ent
        self.check_run_button_state()
        self.ent_widget.setHidden(not self.is_calc_ent)

    def check_run_button_state(self):
        self.run_calculate.setEnabled(self.is_calc_ent or self.is_calc_cor_dim)

    def toggle_calc_cor_dim_cb(self):
        self.is_calc_cor_dim = not self.is_calc_cor_dim
        self.check_run_button_state()
        self.cor_dim_widget.setHidden(not self.is_calc_cor_dim)

    def get_entropy_parameters(self):
        files_list = self.fileNamesEdit.toPlainText().split('\n')
        threshold_value = int(self.rThreshold.text()) if self.is_threshold_used else -1
        dev_coef_value = float(self.rDevCoef.text()) if self.calculateR == CalculationType.DEV else -1
        window_size = int(self.window_size_edit.text()) if self.is_windows_enabled else 0
        step_size = int(self.window_step_edit.text()) if self.is_windows_enabled else 0
        return files_list, threshold_value, dev_coef_value, window_size, step_size

    def get_cor_dim_parameters(self):
        files_list = self.fileNamesEdit.toPlainText().split('\n')
        dimension = int(self.cor_dim_dimension.text())
        radius = float(self.cor_dim_radius.text())
        return files_list, dimension, radius


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
