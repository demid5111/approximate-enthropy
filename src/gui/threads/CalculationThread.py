import math
import time

from PyQt5.QtCore import QThread, pyqtSignal, QThreadPool

from src.core.apen import ApEn
from src.core.report import ReportManager
from src.core.sampen import SampEn
from src.gui.threads.workers.ApEnWorker import AEWorker
from src.gui.threads.workers.CorDimWorker import CDWorker
from src.gui.threads.workers.SampEnWorker import SEWorker


class CalculationThread(QThread):
    done = pyqtSignal(str, str)
    progress = pyqtSignal(int)

    def __init__(self, is_cord_dim_enabled, files_list, dimension,
                 window_size, step_size,
                 cor_dim_radius, is_samp_en, is_ap_en, en_use_threshold,
                 en_threshold_value, en_dev_coef_value, en_calculation_type):
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
        self.res_dic = {}

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def __del__(self):
        self.wait()

    def run(self):
        self.calc(self.is_cord_dim_enabled, self.files_list,
                  self.dimension, self.window_size, self.step_size,
                  self.cor_dim_radius, self.is_samp_en, self.is_ap_en, self.en_use_threshold,
                  self.en_threshold_value, self.en_dev_coef_value, self.en_calculation_type)

    def calc(self, is_cord_dim_enabled, files_list, dimension, window_size, step_size,
             cor_dim_radius=0, is_samp_en=False, is_ap_en=False, en_use_threshold=False,
             en_threshold_value=0, en_dev_coef_value=0, en_calculation_type=0):
        res_dic = {}

        # calculate what is the denominator for progress
        # num files * number of analysis algos
        num_algos = 0
        if is_cord_dim_enabled:
            num_algos += 1
        if is_samp_en:
            num_algos += 1
        if is_ap_en:
            num_algos += 1
        self.full_job = len(files_list) * num_algos

        self.job_index = 0
        for file_name in files_list:
            t0 = time.time()
            res_dic[file_name] = []
            if is_cord_dim_enabled:
                worker = CDWorker(file_name, dimension, cor_dim_radius, window_size, step_size)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

            if is_samp_en:
                worker = SEWorker(dimension, file_name, en_calculation_type, en_dev_coef_value,
                                  en_use_threshold, en_threshold_value, window_size, step_size)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

            if is_ap_en:
                worker = AEWorker(dimension, file_name, en_calculation_type, en_dev_coef_value,
                                  en_use_threshold, en_threshold_value, window_size, step_size)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.receive_report)

            print(time.time() - t0, "seconds per single file")

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
        try:
            self.res_dic[report.get_file_name()].append(report)
        except KeyError:
            self.res_dic[report.get_file_name()] = [report,]
        self.job_index += 1
        self.update_progress(self.full_job, self.job_index)