import math

from PyQt5.QtCore import QThread, pyqtSignal, QThreadPool, QMutex

from src.core.apen_opt import ApproximateEntropy
from src.core.cordim import CorDim
from src.core.fracdim import FracDim
from src.core.report import ReportManager
from src.core.sampen_opt import SampleEntropy
from src.gui.threads.workers.GeneralWorker import GeneralWorker


class CalculationThread(QThread):
    done = pyqtSignal(str, str)
    progress = pyqtSignal(int)

    def __init__(self, is_cord_dim_enabled, files_list, dimension,
                 window_size, step_size,
                 cor_dim_radius, is_samp_en, is_ap_en, en_use_threshold,
                 en_threshold_value, en_dev_coef_value, en_calculation_type,
                 is_frac_dim_enabled, fd_max_k):
        QThread.__init__(self)
        self.is_cord_dim_enabled = is_cord_dim_enabled
        self.files_list = files_list
        self.dimension = dimension
        self.window_size = window_size
        self.step_size = step_size
        self.cor_dim_radius = cor_dim_radius
        self.is_samp_en = is_samp_en
        self.is_ap_en = is_ap_en
        self.en_use_threshold = en_use_threshold
        self.en_threshold_value = en_threshold_value
        self.en_dev_coef_value = en_dev_coef_value
        self.en_calculation_type = en_calculation_type
        self.is_frac_dim_enabled = is_frac_dim_enabled
        self.fd_max_k = fd_max_k

        self.res_dic = {}
        self.mutex = QMutex()
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def __del__(self):
        self.wait()

    def run(self):
        self.calc(self.is_cord_dim_enabled, self.files_list,
                  self.dimension, self.window_size, self.step_size,
                  self.cor_dim_radius, self.is_samp_en, self.is_ap_en, self.en_use_threshold,
                  self.en_threshold_value, self.en_dev_coef_value, self.en_calculation_type,
                  self.is_frac_dim_enabled, self.fd_max_k)

    def calc(self, is_cord_dim_enabled, files_list, dimension, window_size, step_size,
             cor_dim_radius=0, is_samp_en=False, is_ap_en=False, en_use_threshold=False,
             en_threshold_value=0, en_dev_coef_value=0, en_calculation_type=0,
             is_frac_dim_enabled=False, fd_max_k=0):
        # calculate what is the denominator for progress
        # num files * number of analysis algos
        num_algos = 0
        if is_cord_dim_enabled:
            num_algos += 1
        if is_frac_dim_enabled:
            num_algos += 1
        if is_samp_en:
            num_algos += 1
        if is_ap_en:
            num_algos += 1
        self.full_job = len(files_list) * num_algos

        self.job_index = 0
        for file_name in files_list:
            if is_cord_dim_enabled:
                worker = GeneralWorker(CorDim.prepare_calculate_window_cor_dim,
                                       file_name, dimension, cor_dim_radius, window_size, step_size)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

            if is_frac_dim_enabled:
                worker = GeneralWorker(FracDim.prepare_calculate_window_frac_dim,
                                       file_name, fd_max_k,
                                       window_size, step_size)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

            if is_samp_en:
                worker = GeneralWorker(SampleEntropy.prepare_calculate_windowed,
                                       dimension, file_name, en_calculation_type, en_dev_coef_value,
                                       en_use_threshold, en_threshold_value, window_size, step_size)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

            if is_ap_en:
                worker = GeneralWorker(ApproximateEntropy.prepare_calculate_windowed,
                                       dimension, file_name, en_calculation_type, en_dev_coef_value,
                                       en_use_threshold, en_threshold_value, window_size, step_size)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

        self.threadpool.waitForDone()
        self.job_index = -1
        self.full_job = -1
        analysis_names = ReportManager.get_analysis_types(self.res_dic)
        self.done.emit(','.join(analysis_names), ','.join(list(self.res_dic.keys())))
        ReportManager.prepare_write_report(analysis_types=analysis_names, res_dic=self.res_dic)

    def update_progress(self, full, current):
        progress = math.ceil((current / full) * 100)
        self.progress.emit(progress)

    def receive_report(self, report):
        self.mutex.lock()
        try:
            self.res_dic[report.get_file_name()].append(report)
        except KeyError:
            self.res_dic[report.get_file_name()] = [report, ]

        self.job_index += 1
        self.update_progress(self.full_job, self.job_index)
        self.mutex.unlock()
