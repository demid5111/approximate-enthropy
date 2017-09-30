from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton, QGridLayout, QLabel, QCheckBox, \
    QLineEdit, QMessageBox, QProgressBar

from src.gui.threads.CalculationThread import CalculationThread
from src.gui.widgets.cor_dim_widget import CorDimWidget

from src.gui.widgets.entropy_widget import EntropyWidget
from src.gui.widgets.file_chooser_widget import FileChooserWidget


class ApEnWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.fileName = ".memory"
        self.files_selected = True  # represent if FileChooserWidget has any files selected
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

        self.file_chooser_widget = FileChooserWidget(self, self.fileName)
        self.file_chooser_widget.new_files_chosen.connect(self.on_new_files_chosen)
        self.file_chooser_widget.erased_files.connect(self.on_erased_files)
        grid.addWidget(self.file_chooser_widget, 7, 0, 1, 3)

        grid.addWidget(self.run_calculate, 10, 0, 1, 3)

        # Creating a label
        self.progress_label = QLabel('Calculation progress', self)

        # Creating a progress bar and setting the value limits
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimum(0)
        grid.addWidget(self.progress_label, 14, 0)
        grid.addWidget(self.progress_bar, 14, 1)

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

        cor_dim_radius = self.cor_dim_widget.get_radius() if is_cord_dim_enabled else 0
        is_samp_en = self.ent_widget.is_samp_en() if is_ent_enabled else False
        is_ap_en = self.ent_widget.is_ap_en() if is_ent_enabled else False
        en_threshold_value, en_dev_coef_value, en_calculation_type, en_use_threshold = (self.get_entropy_parameters()
                                                                                        if is_ent_enabled else [0, 0, 0,
                                                                                                                0])
        self.calc_thread = CalculationThread(is_cord_dim_enabled, files_list, dimension,
                                             window_size, step_size,
                                             cor_dim_radius, is_samp_en, is_ap_en, en_use_threshold,
                                             en_threshold_value, en_dev_coef_value, en_calculation_type)

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
                "{} calculated for: \n {}".format(source, "".join(["- {}, \n".format(i) for i in file_names.split(',')])))
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

    def toggle_window_checkbox(self):
        self.is_windows_enabled = not self.is_windows_enabled
        self.window_size_edit.setEnabled(self.is_windows_enabled)
        self.window_step_edit.setEnabled(self.is_windows_enabled)

    def check_run_button_state(self):
        self.run_calculate.setEnabled((self.is_calc_ent or self.is_calc_cor_dim) and
                                      self.files_selected and not self.is_in_progress)

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
