import os

import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton, QGridLayout, QLabel, QCheckBox, \
    QLineEdit, QMessageBox

from src.core.report import CorDimReport, SampEnReport, ApEnReport, ReportManager
from src.gui.widgets.cor_dim_widget import CorDimWidget

from src.core.apen import ApEn
from src.core.cordim import CorDim
from src.core.sampen import SampEn
from src.gui.widgets.entropy_widget import EntropyWidget
from src.gui.widgets.file_chooser_widget import FileChooserWidget


class ApEnWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.fileName = ".memory"
        self.files_selected = False # represent if FileChooserWidget has any files selected
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tabs.resize(500, 600)

        # Add tabs
        self.tabs.addTab(self.tab1, "Entropy")

        # Create first tab
        enth_grid = self.config_entropy_tab()

        self.tab1.setLayout(enth_grid)

        # Add tabs to widget
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def config_entropy_tab(self):
        mLabel = QLabel('m')
        self.mEdit = QLineEdit("2")
        window_cb = QCheckBox('Use windows', self)
        window_cb.setChecked(True)
        window_cb.clicked.connect(self.toggle_window_checkbox)
        self.window_size_edit = QLineEdit("100")
        self.window_step_edit = QLineEdit("10")
        self.is_windows_enabled = True

        self.is_use_ent_cb = QCheckBox('Calculate entropy?', self)
        self.is_calc_ent = True
        self.is_use_ent_cb.setChecked(self.is_calc_ent)
        self.is_use_ent_cb.clicked.connect(self.toggle_calc_ent_cb)

        self.ent_widget = EntropyWidget(self)

        self.is_use_cor_dim_cb = QCheckBox('Calculate cor dim?', self)
        self.is_calc_cor_dim = True
        self.is_use_cor_dim_cb.setChecked(self.is_calc_cor_dim)
        self.is_use_cor_dim_cb.clicked.connect(self.toggle_calc_cor_dim_cb)

        self.run_calculate = QPushButton("Run calculation", self)
        self.run_calculate.clicked.connect(self.calculate)

        grid = QGridLayout()
        grid.addWidget(mLabel, 0, 0)
        grid.addWidget(self.mEdit, 0, 1)
        grid.addWidget(window_cb, 1, 0)
        grid.addWidget(self.window_size_edit, 1, 1)
        grid.addWidget(self.window_step_edit, 2, 1)
        grid.addWidget(self.is_use_ent_cb, 3, 0)
        grid.addWidget(self.ent_widget, 4, 1)
        grid.addWidget(self.is_use_cor_dim_cb, 5, 0)

        self.cor_dim_widget = CorDimWidget(self)
        grid.addWidget(self.cor_dim_widget, 6, 1)

        grid.addWidget(self.run_calculate, 10, 0, 3, 3)

        self.file_chooser_widget = FileChooserWidget(self, self.fileName)
        self.file_chooser_widget.new_files_chosen.connect(self.on_new_files_chosen)
        self.file_chooser_widget.erased_files.connect(self.on_erased_files)
        grid.addWidget(self.file_chooser_widget, 7, 0, 1, 3)

        return grid

    def on_new_files_chosen(self):
        self.files_selected = True

    def on_erased_files(self):
        self.files_selected = False

    def calculate(self):
        is_ent_enabled = self.is_use_ent_cb
        is_cord_dim_enabled = self.is_use_cor_dim_cb

        files_list = self.file_chooser_widget.get_file_names()
        dimension = int(self.mEdit.text())
        window_size = self.get_window_size()
        step_size = self.get_step_size()

        res_dic = {}
        for file_name in files_list:
            t0 = time.time()
            res_dic[file_name] = []
            if is_cord_dim_enabled:
                res = self.calc_cor_dim_wrapper(file_name, dimension, window_size, step_size)
                res_dic[file_name].append(res)

            if is_ent_enabled:
                is_samp_en = self.ent_widget.is_samp_en()
                is_ap_en = self.ent_widget.is_ap_en()
                threshold_value, dev_coef_value, calculation_type, use_threshold = self.get_entropy_parameters()

                if is_samp_en:
                    res = self.calc_sampen_wrapper(file_name, dimension, window_size, step_size, calculation_type,
                                                   dev_coef_value, use_threshold, threshold_value)
                    res_dic[file_name].append(res)

                if is_ap_en:
                    res = self.calc_apen_wrapper(file_name, dimension, window_size, step_size, calculation_type,
                                                 dev_coef_value, use_threshold, threshold_value)
                    res_dic[file_name].append(res)
            print(time.time() - t0, "seconds wall time")
        analysis_names = ReportManager.get_analysis_types(res_dic)
        self.show_message(','.join(analysis_names), res_dic)
        ReportManager.prepare_write_report(analysis_types=analysis_names, res_dic=res_dic)

    def calc_cor_dim_wrapper(self, file_name, dimension, window_size, step_size):
        radius = self.cor_dim_widget.get_radius()
        tmp = CorDim()

        try:
            res = tmp.prepare_calculate_window_cor_dim(file_name, dimension, radius, window_size, step_size)
        except ValueError:
            res = CorDimReport()
            res.set_error("Error! For file {}".format(file_name))

        return res

    def calc_sampen_wrapper(self, file_name, dimension, window_size, step_size, calculation_type,
                            dev_coef_value, use_threshold, threshold_value):
        tmp = SampEn()
        try:
            res = tmp.prepare_calculate_window_sampen(m=dimension,
                                                      file_name=file_name,
                                                      calculation_type=calculation_type,
                                                      dev_coef_value=dev_coef_value,
                                                      use_threshold=use_threshold,
                                                      threshold_value=threshold_value,
                                                      window_size=window_size,
                                                      step_size=step_size)
        except ValueError:
            res = SampEnReport()
            res.set_error("Error! For file {}".format(file_name))
        return res

    def calc_apen_wrapper(self, file_name, dimension, window_size, step_size, calculation_type,
                          dev_coef_value, use_threshold, threshold_value):
        tmp = ApEn()
        try:
            res = tmp.prepare_calculate_window_apen(m=dimension,
                                                    file_name=file_name,
                                                    calculation_type=calculation_type,
                                                    dev_coef_value=dev_coef_value,
                                                    use_threshold=use_threshold,
                                                    threshold_value=threshold_value,
                                                    window_size=window_size,
                                                    step_size=step_size)
        except ValueError:
            res = ApEnReport()
            res.set_error("Error! For file {}".format(file_name))
        return res

    def show_message(self, source, res_dic):
        dialog = QMessageBox(self)
        dialog.setWindowModality(False)
        dialog.setText(
                "{} calculated for: \n {}".format(source, "".join(["- {}, \n".format(i) for i in res_dic.keys()])))
        dialog.show()

    def toggle_calc_ent_cb(self):
        self.is_calc_ent = not self.is_calc_ent
        self.ent_widget.set_ap_en(self.is_calc_ent)
        self.ent_widget.set_samp_en(self.is_calc_ent)
        self.check_run_button_state()
        self.ent_widget.setHidden(not self.is_calc_ent)

    def toggle_window_checkbox(self):
        self.is_windows_enabled = not self.is_windows_enabled
        self.window_size_edit.setEnabled(self.is_windows_enabled)
        self.window_step_edit.setEnabled(self.is_windows_enabled)

    def check_run_button_state(self):
        self.run_calculate.setEnabled((self.is_calc_ent or self.is_calc_cor_dim) and self.files_selected)

    def toggle_calc_cor_dim_cb(self):
        self.is_calc_cor_dim = not self.is_calc_cor_dim
        self.check_run_button_state()
        self.cor_dim_widget.setHidden(not self.is_calc_cor_dim)

    def get_entropy_parameters(self):
        threshold_value = self.ent_widget.get_threshold()
        dev_coef_value = self.ent_widget.get_dev_coef_value()
        calculation_type = self.ent_widget.get_calculation_type()
        use_threshold = self.ent_widget.is_threshold()
        return threshold_value, dev_coef_value, calculation_type, use_threshold

    def get_window_size(self):
        return int(self.window_size_edit.text()) if self.is_windows_enabled else 0

    def get_step_size(self):
        return int(self.window_step_edit.text()) if self.is_windows_enabled else 0
