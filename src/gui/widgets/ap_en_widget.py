from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton, QGridLayout, QLabel, QCheckBox, \
    QLineEdit, QMessageBox, QProgressBar

from src.gui.threads.CalculationThread import CalculationThread
from src.gui.widgets.cor_dim_widget import CorDimWidget

from src.gui.widgets.entropy_widget import EntropyWidget
from src.gui.widgets.file_chooser_widget import FileChooserWidget
from src.gui.widgets.frac_dim_widget import FracDimWidget
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

        window_cb = QCheckBox('Use sliding windows', self)
        self.is_windows_enabled = True
        window_cb.setChecked(self.is_windows_enabled)
        window_cb.clicked.connect(self.toggle_window_checkbox)

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
        grid.addWidget(window_cb, 1, 0)
        grid.addWidget(self.window_analysis_widget, 2, 1)
        grid.addWidget(self.is_use_ent_cb, 3, 0)
        grid.addWidget(self.ent_widget, 4, 1)

        grid.addWidget(self.is_use_pertropy_cb, 5, 0)

        self.cor_dim_widget = CorDimWidget(self)
        grid.addWidget(self.is_use_cor_dim_cb, 6, 0)
        grid.addWidget(self.cor_dim_widget, 7, 1)

        self.frac_dim_widget = FracDimWidget(self)
        grid.addWidget(self.is_use_frac_dim_cb, 8, 0)
        grid.addWidget(self.frac_dim_widget, 9, 1)

        self.file_chooser_widget = FileChooserWidget(self, self.fileName)
        self.file_chooser_widget.new_files_chosen.connect(self.on_new_files_chosen)
        self.file_chooser_widget.erased_files.connect(self.on_erased_files)
        grid.addWidget(self.file_chooser_widget, 10, 0, 1, 3)

        grid.addWidget(self.run_calculate, 13, 0, 1, 3)

        # Creating a label
        self.progress_label = QLabel('Calculation progress', self)

        # Creating a progress bar and setting the value limits
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimum(0)
        grid.addWidget(self.progress_label, 17, 0)
        grid.addWidget(self.progress_bar, 17, 1)

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

        self.calc_thread = CalculationThread(is_cord_dim_enabled, files_list, dimension,
                                             window_size, step_size,
                                             cor_dim_radius, is_samp_en, is_ap_en, en_use_threshold,
                                             en_threshold_value, en_dev_coef_value, en_calculation_type,
                                             is_frac_dim_enabled, fd_max_k, is_pertropy_enabled)

        self.set_in_progress(True)
        self.calc_thread.done.connect(self.show_message)
        self.calc_thread.done.connect(self.erase_in_progress)
        self.calc_thread.progress.connect(self.track_ui_progress)
        self.calc_thread.start()

    def track_ui_progress(self, val):
        self.progress_bar.setValue(val)

    def show_message(self, source, file_names):
        dialog = QMessageBox(self)
        dialog.setWindowModality(False)
        dialog.setText(
                "{} calculated for: \n {}".format(source, "".join(["- {} \n".format(i) for i in file_names.split(',')])))
        dialog.show()

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
        self.check_run_button_state()
        self.ent_widget.setHidden(not self.is_calc_ent)

    def toggle_calc_pertropy_cb(self):
        self.is_calc_pertropy = not self.is_calc_pertropy

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
        return int(self.window_analysis_widget.get_window_size()) if self.is_windows_enabled else 0

    def get_step_size(self):
        return int(self.window_analysis_widget.get_window_step()) if self.is_windows_enabled else 0
