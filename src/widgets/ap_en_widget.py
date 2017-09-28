import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton, QGridLayout, QLabel, QTextEdit, QCheckBox, \
    QLineEdit, QFileDialog, QMessageBox

from src.core.apen import ApEn
from src.core.cordim import CorDim
from src.core.sampen import SampEn
from src.utils.supporting import CalculationType
from src.widgets.cor_dim_widget import CorDimWidget
from src.widgets.entropy_widget import EntropyWidget


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

        # Create first tab
        enth_grid = self.config_entropy_tab()

        self.tab1.setLayout(enth_grid)

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

        grid = QGridLayout()
        grid.addWidget(cb, 0, 0)
        grid.addWidget(self.rThreshold, 0, 1)
        grid.addWidget(window_cb, 1, 0)
        grid.addWidget(self.window_size_edit, 1, 1)
        grid.addWidget(self.window_step_edit, 2, 1)
        grid.addWidget(rLabel, 3, 0)

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

        grid = QGridLayout()
        grid.addWidget(mLabel, 0, 0)
        grid.addWidget(self.mEdit, 0, 1)
        grid.addWidget(self.is_use_ent_cb, 1, 1)
        grid.addWidget(self.ent_widget, 2, 1)
        grid.addWidget(self.is_use_cor_dim_cb, 3, 1)
        grid.addWidget(self.cor_dim_widget, 4, 1)
        grid.addWidget(self.run_calculate, 8, 1, 3, 1)

        file_chooser_group = self.config_filechooser_group()
        grid.addLayout(file_chooser_group, 5, 0, 1, 3)

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
        self.check_run_button_state()

    def calculate(self):
        is_ent_enabled = self.is_use_ent_cb
        is_cord_dim_enabled = self.is_use_cor_dim_cb

        files_list = self.get_file_names()
        dimension = int(self.mEdit.text())

        if is_cord_dim_enabled:
            radius = self.cor_dim_widget.get_radius()
            res_dic = {}
            tmp = CorDim()
            for file_name in files_list:
                try:
                    res = tmp.calculate_cor_dim(file_name, dimension, radius)
                    res_dic[file_name] = res
                except ValueError:
                    res_dic[file_name] = {'error': "Error! For file {}".format(file_name)}

            self.show_message('CorDim', res_dic)
            make_report(res_dic=res_dic, is_ap_en=False)

        if is_ent_enabled:
            is_samp_en = self.ent_widget.is_samp_en()
            is_ap_en = self.ent_widget.is_ap_en()
            (threshold_value, dev_coef_value, window_size, step_size,
             calculation_type, use_threshold) = self.get_entropy_parameters()

            if is_samp_en:
                res_dic = {}
                tmp = SampEn()
                for file_name in files_list:
                    try:
                        res = tmp.prepare_calculate_window_sampen(m=dimension,
                                                                  file_name=file_name,
                                                                  calculation_type=calculation_type,
                                                                  dev_coef_value=dev_coef_value,
                                                                  use_threshold=use_threshold,
                                                                  threshold_value=threshold_value,
                                                                  window_size=window_size,
                                                                  step_size=step_size)
                        res_dic[file_name] = res
                    except ValueError:
                        res_dic[file_name] = {'error': "Error! For file {}".format(file_name)}

                self.show_message('SampEn', res_dic)
                make_report(res_dic=res_dic, is_ap_en=False)

            if is_ap_en:
                res_dic = {}
                tmp = ApEn()
                for file_name in files_list:
                    try:
                        res = tmp.prepare_calculate_window_apen(m=dimension,
                                                                file_name=file_name,
                                                                calculation_type=calculation_type,
                                                                dev_coef_value=dev_coef_value,
                                                                use_threshold=use_threshold,
                                                                threshold_value=threshold_value,
                                                                window_size=window_size,
                                                                step_size=step_size)
                        res_dic[file_name] = res
                    except ValueError:
                        res_dic[file_name] = {'error': "Error! For file {}".format(file_name)}
                self.show_message('ApEn', res_dic)
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
        self.check_run_button_state()

    def memorize_last_path(self):
        if not self.fileNamesEdit:
            return
        path = os.path.dirname(self.fileNamesEdit.toPlainText().split('\n')[0])
        with open(self.fileName, "w") as f:
            f.write(path + '/')

    def toggle_calc_ent_cb(self):
        self.is_calc_ent = not self.is_calc_ent
        self.ent_widget.set_ap_en(self.is_calc_ent)
        self.ent_widget.set_samp_en(self.is_calc_ent)
        self.check_run_button_state()
        self.ent_widget.setHidden(not self.is_calc_ent)

    def get_file_names(self):
        return [x for x in self.fileNamesEdit.toPlainText().split('\n') if x]

    def check_run_button_state(self):
        self.run_calculate.setEnabled((self.is_calc_ent or self.is_calc_cor_dim) and len(self.get_file_names()) > 0)

    def toggle_calc_cor_dim_cb(self):
        self.is_calc_cor_dim = not self.is_calc_cor_dim
        self.check_run_button_state()
        self.cor_dim_widget.setHidden(not self.is_calc_cor_dim)

    def get_entropy_parameters(self):
        threshold_value = self.ent_widget.get_threshold()
        dev_coef_value = self.ent_widget.get_dev_coef_value()
        window_size = self.ent_widget.get_window_size()
        step_size = self.ent_widget.get_step_size()
        calculation_type = self.ent_widget.get_calculation_type()
        use_threshold = self.ent_widget.is_threshold()
        return threshold_value, dev_coef_value, window_size, step_size, calculation_type, use_threshold


def make_report(file_name="results/results.csv", res_dic=None, is_ap_en=True):
    if not res_dic:
        print("Error in generating report")
    with open(file_name, "w") as f:
        f.write('Entropy type, {}\n'.format('Approximate Entropy' if is_ap_en else 'Sample Entropy'))

        # get sample size of window and step
        any_key = list(res_dic.keys())[0]
        f.write('Window size, {}\n'.format(ApEn.get_n_val(res_dic[any_key])))
        f.write('Step size, {}\n'.format(ApEn.get_step_size_val(res_dic[any_key])))

        f.write(','.join(['File name', 'Window number', 'Entropy', 'R', 'Average RR']) + '\n')

        for (file_name, ind_result) in res_dic.items():
            try:
                ApEn.get_err_val(ind_result)
                f.write(','.join([file_name, ApEn.get_err_val(ind_result)]) + '\n')
                continue
            except KeyError:
                pass
            for (window_index, res_val) in enumerate(ApEn.get_result_val(ind_result)):
                res_list = ['{}'.format(file_name),  # empty for filename column
                            str(window_index),
                            str('{0:.10f}'.format(res_val)),
                            str(ApEn.get_r_val(ind_result)[window_index]),
                            str(ApEn.get_avg_rr_val(ind_result)[window_index])]
                f.write(','.join(res_list) + '\n')
