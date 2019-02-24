from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton, QGridLayout, QLabel, QCheckBox, \
    QLineEdit, QMessageBox, QProgressBar

from src.gui.threads.CalculationThread import CalculationThread
from src.gui.widgets.cor_dim_widget import CorDimWidget

from src.gui.widgets.entropy_widget import EntropyWidget
from src.gui.widgets.file_chooser_widget import FileChooserWidget
from src.gui.widgets.frac_dim_widget import FracDimWidget
from src.gui.widgets.pertropy_widget import PertropyWidget
from src.gui.widgets.window_analysis_widget import WindowAnalysisWidget


class ApEnWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.fileName = ".memory"
        self.files_selected = False  # represent if FileChooserWidget has any files selected
        self.is_in_progress = False  # represent if calculation is in progress
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
        self.check_run_button_state()

    def config_entropy_tab(self):
        mLabel = QLabel('m (length of vectors)<br>or n (for pertropy only) ')
        self.mEdit = QLineEdit("2")

        self.window_cb = QCheckBox('Use sliding windows', self)
        self.is_windows_enabled = True
        self.window_cb.setChecked(self.is_windows_enabled)
        self.window_cb.clicked.connect(self.toggle_window_checkbox)

        self.window_analysis_widget = WindowAnalysisWidget(self)

        self.is_use_ent_cb = QCheckBox('Calculate Sample/Approximate Entropy?', self)
        self.is_calc_ent = True
        self.is_use_ent_cb.setChecked(self.is_calc_ent)
        self.is_use_ent_cb.clicked.connect(self.toggle_calc_ent_cb)

        self.ent_widget = EntropyWidget(self)

        self.is_use_pertropy_cb = QCheckBox('Calculate Permutation Entropy?', self)
        self.is_calc_pertropy = True
        self.is_use_pertropy_cb.setChecked(self.is_calc_pertropy)
        self.is_use_pertropy_cb.clicked.connect(self.toggle_calc_pertropy_cb)

        self.pertropy_widget = PertropyWidget(self)

        self.is_use_cor_dim_cb = QCheckBox('Calculate correlation dimension?', self)
        self.is_calc_cor_dim = True
        self.is_use_cor_dim_cb.setChecked(self.is_calc_cor_dim)
        self.is_use_cor_dim_cb.clicked.connect(self.toggle_calc_cor_dim_cb)

        self.is_use_frac_dim_cb = QCheckBox('Calculate fractal dimension?', self)
        self.is_calc_frac_dim = True
        self.is_use_frac_dim_cb.setChecked(self.is_calc_cor_dim)
        self.is_use_frac_dim_cb.clicked.connect(self.toggle_calc_frac_dim_cb)

        self.run_calculate = QPushButton("Run calculation", self)
        self.run_calculate.clicked.connect(self.calculate)

        grid = QGridLayout()
        grid.addWidget(mLabel, 0, 0)
        grid.addWidget(self.mEdit, 0, 1)
        grid.addWidget(self.window_cb, 0, 3)
        grid.addWidget(self.window_analysis_widget, 1, 4)
        grid.addWidget(self.is_use_ent_cb, 2, 0)
        grid.addWidget(self.ent_widget, 3, 1)

        grid.addWidget(self.is_use_pertropy_cb, 2, 3)
        grid.addWidget(self.pertropy_widget, 3, 4)

        self.cor_dim_widget = CorDimWidget(self)
        grid.addWidget(self.is_use_cor_dim_cb, 4, 3)
        grid.addWidget(self.cor_dim_widget, 5, 4)

        self.frac_dim_widget = FracDimWidget(self)
        grid.addWidget(self.is_use_frac_dim_cb, 6, 3)
        grid.addWidget(self.frac_dim_widget, 7, 4)

        self.file_chooser_widget = FileChooserWidget(self, self.fileName)
        self.file_chooser_widget.new_files_chosen.connect(self.on_new_files_chosen)
        self.file_chooser_widget.erased_files.connect(self.on_erased_files)
        grid.addWidget(self.file_chooser_widget, 4, 0, 5, 3)

        grid.addWidget(self.run_calculate, 14, 0, 1, 3)

        # Creating a label
        self.progress_label = QLabel('Calculation progress', self)

        # Creating a progress bar and setting the value limits
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimum(0)
        grid.addWidget(self.progress_label, 18, 0)
        grid.addWidget(self.progress_bar, 18, 1)

        return grid

    def on_new_files_chosen(self):
        self.files_selected = True
        self.check_run_button_state()

    def on_erased_files(self):
        self.files_selected = False
        self.check_run_button_state()

    def calculate(self):
        is_ent_enabled = self.is_use_ent_cb.isChecked()
        is_cord_dim_enabled = self.is_use_cor_dim_cb.isChecked()
        is_frac_dim_enabled = self.is_use_frac_dim_cb.isChecked()
        is_pertropy_enabled = self.is_use_pertropy_cb.isChecked()
        is_pertropy_normalized = self.pertropy_widget.is_normalize_used
        is_pertropy_stride = self.pertropy_widget.is_stride_used

        files_list = self.file_chooser_widget.get_file_names()
        dimension = int(self.mEdit.text())
        window_size = self.get_window_size()
        step_size = self.get_step_size()

        cor_dim_radius = self.cor_dim_widget.get_radius() if is_cord_dim_enabled else 0
        is_samp_en = self.ent_widget.is_samp_en() if is_ent_enabled else False
        is_ap_en = self.ent_widget.is_ap_en() if is_ent_enabled else False
        en_threshold_value, en_dev_coef_value, en_calculation_type, en_use_threshold = (self.get_entropy_parameters()
                                                                                        if is_ent_enabled else [0, 0, 0,
                                                                                                                0])
        fd_max_k = self.get_frac_dim_parameters() if is_frac_dim_enabled else 0
        pertropy_stride = self.pertropy_widget.get_stride() if is_pertropy_stride else 1

        self.calc_thread = CalculationThread(is_cord_dim_enabled, files_list, dimension,
                                             window_size, step_size,
                                             cor_dim_radius, is_samp_en, is_ap_en, en_use_threshold,
                                             en_threshold_value, en_dev_coef_value, en_calculation_type,
                                             is_frac_dim_enabled, fd_max_k,
                                             is_pertropy_enabled, is_pertropy_normalized, pertropy_stride)

        self.set_in_progress(True)
        self.calc_thread.done.connect(self.show_message)
        self.calc_thread.done.connect(self.erase_in_progress)
        self.calc_thread.progress.connect(self.track_ui_progress)
        self.calc_thread.start()

    def track_ui_progress(self, val):
        self.progress_bar.setValue(val if val < 100 else 0)

    def show_message(self, source, file_names, report_path=None):
        self.ok_button = QPushButton('Ok', self)
        self.dialog = QMessageBox(self)
        self.dialog.setWindowModality(False)
        all_files = "".join(["- {} \n".format(i) for i in file_names.split(',')])
        dialog_text = "{} calculated for: \n {}".format(source, all_files)
        if report_path:
            dialog_text += '\n Saved report in {}'.format(report_path)
        self.dialog.setText(dialog_text)
        self.dialog.setDefaultButton(self.ok_button)
        self.dialog.show()

    def set_in_progress(self, v):
        self.is_in_progress = v
        self.track_ui_progress(0)
        self.check_run_button_state()

    def erase_in_progress(self):
        self.set_in_progress(False)

    def toggle_calc_ent_cb(self):
        self.is_calc_ent = not self.is_calc_ent
        self.ent_widget.set_ap_en(self.is_calc_ent)
        self.ent_widget.set_samp_en(self.is_calc_ent)
        if not self.is_calc_ent:
            self.ent_widget.reset_to_default()
        self.check_run_button_state()
        self.ent_widget.setHidden(not self.is_calc_ent)

    def toggle_calc_pertropy_cb(self):
        self.is_calc_pertropy = not self.is_calc_pertropy
        self.check_run_button_state()
        self.pertropy_widget.setHidden(not self.is_calc_pertropy)
        if not self.is_calc_pertropy:
            self.pertropy_widget.reset_to_default()

    def toggle_window_checkbox(self):
        self.is_windows_enabled = not self.is_windows_enabled
        self.window_analysis_widget.setHidden(not self.is_windows_enabled)

    def check_run_button_state(self):
        any_algo_used = self.is_calc_ent or self.is_calc_cor_dim or self.is_calc_frac_dim or self.is_calc_pertropy
        self.run_calculate.setEnabled(any_algo_used and
                                      self.files_selected and not self.is_in_progress)

    def toggle_calc_cor_dim_cb(self):
        self.is_calc_cor_dim = not self.is_calc_cor_dim
        self.check_run_button_state()
        self.cor_dim_widget.setHidden(not self.is_calc_cor_dim)

    def toggle_calc_frac_dim_cb(self):
        self.is_calc_frac_dim = not self.is_calc_frac_dim
        self.check_run_button_state()
        self.frac_dim_widget.setHidden(not self.is_calc_frac_dim)

    def get_entropy_parameters(self):
        threshold_value = self.ent_widget.get_threshold()
        dev_coef_value = self.ent_widget.get_dev_coef_value()
        calculation_type = self.ent_widget.get_calculation_type()
        use_threshold = self.ent_widget.is_threshold()
        return threshold_value, dev_coef_value, calculation_type, use_threshold

    def get_frac_dim_parameters(self):
        fd_max_k = self.frac_dim_widget.get_max_k()
        return fd_max_k

    def get_window_size(self):
        return int(self.window_analysis_widget.get_window_size()) if self.is_windows_enabled else None

    def get_step_size(self):
        return int(self.window_analysis_widget.get_window_step()) if self.is_windows_enabled else None
