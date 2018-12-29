import math

from PyQt5.QtCore import QThread, pyqtSignal, QThreadPool, QMutex, QEventLoop, QTimer

from src.core.apen_opt import ApproximateEntropy
from src.core.cordim import CorDim
from src.core.fracdim import FracDim
from src.core.permen import PermutationEntropy
from src.core.report import ReportManager
from src.core.sampen_opt import SampleEntropy
from src.gui.threads.workers.GeneralWorker import GeneralWorker


class CalculationThread(QThread):
    done = pyqtSignal(str, str, str)
    progress = pyqtSignal(int)

    def __init__(self, is_cord_dim_enabled, files_list, dimension,
                 window_size, step_size,
                 cor_dim_radius, is_samp_en, is_ap_en, en_use_threshold,
                 en_threshold_value, en_dev_coef_value, en_calculation_type,
                 is_frac_dim_enabled, fd_max_k, is_pertropy_enabled, is_pertropy_normalized):
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
        self.is_pertropy_enabled = is_pertropy_enabled
        self.is_pertropy_normalized = is_pertropy_normalized

        self.res_dic = {}
        self.mutex = QMutex()
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.print_my_configuration()

    def __del__(self):
        self.wait()

    def run(self):
        self.calc(self.is_cord_dim_enabled, self.files_list,
                  self.dimension, self.window_size, self.step_size,
                  self.cor_dim_radius, self.is_samp_en, self.is_ap_en, self.en_use_threshold,
                  self.en_threshold_value, self.en_dev_coef_value, self.en_calculation_type,
                  self.is_frac_dim_enabled, self.fd_max_k,
                  self.is_pertropy_enabled, self.is_pertropy_normalized)

    def calc(self, is_cord_dim_enabled, files_list, dimension, window_size, step_size,
             cor_dim_radius=0, is_samp_en=False, is_ap_en=False, en_use_threshold=False,
             en_threshold_value=0, en_dev_coef_value=0, en_calculation_type=0,
             is_frac_dim_enabled=False, fd_max_k=0,
             is_pertropy_enabled=False, is_pertropy_normalized=False):
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
        if is_pertropy_enabled:
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
                                       dimension, file_name,
                                       en_use_threshold, en_threshold_value,
                                       window_size, step_size,
                                       en_calculation_type, en_dev_coef_value)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

            if is_ap_en:
                worker = GeneralWorker(ApproximateEntropy.prepare_calculate_windowed,
                                       dimension, file_name,
                                       en_use_threshold, en_threshold_value,
                                       window_size, step_size,
                                       en_calculation_type, en_dev_coef_value)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

            if is_pertropy_enabled:
                worker = GeneralWorker(PermutationEntropy.prepare_calculate_windowed,
                                       dimension, file_name,
                                       en_use_threshold, en_threshold_value,
                                       window_size, step_size,
                                       None, None,
                                       is_pertropy_normalized)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

    def on_threads_completed(self):
        self.threadpool.waitForDone()
        self.job_index = 0
        self.full_job = 0

        if not self.res_dic:
            self.done.emit('Error', 'Result is empty', None)
            return

        analysis_names = ReportManager.get_analysis_types(self.res_dic)
        ReportManager.prepare_write_report(analysis_types=analysis_names, res_dic=self.res_dic)

        all_analysis_names = ','.join(analysis_names)
        all_files_names = ','.join(list(self.res_dic.keys()))
        self.done.emit(all_analysis_names, all_files_names, ReportManager.get_report_path())

    def update_progress(self, full, current):
        progress = math.ceil((current / full) * 100)
        if progress == 100:
            self.on_threads_completed()
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

    def print_my_configuration(self):
        print('m: {}'.format(self.dimension))
        print('window size: {}'.format(self.window_size))
        print('step size: {}'.format(self.step_size))
        print('calculating cordim: {}'.format(self.is_cord_dim_enabled))
        print('cordim radius: {}'.format(self.cor_dim_radius))
        print('calculating apen: {}'.format(self.is_ap_en))
        print('calculating sampen: {}'.format(self.is_samp_en))
        print('using threshold: {}'.format(self.en_use_threshold))
        print('threshold: {}'.format(self.en_threshold_value))
        print('r type: {}'.format(self.en_calculation_type))
        print('r dev coef: {}'.format(self.en_dev_coef_value))
        print('calculating fracdim: {}'.format(self.is_frac_dim_enabled))
        print('fracdim max k: {}'.format(self.fd_max_k))
        print('calculating pertropy: {}'.format(self.is_pertropy_enabled))
