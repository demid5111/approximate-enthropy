import time

import math
from PyQt5.QtCore import QThread, pyqtSignal

from src.core.apen import ApEn
from src.core.cordim import CorDim
from src.core.report import ReportManager
from src.core.sampen import SampEn


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
        full_job = len(files_list) * num_algos

        job_index = 0
        for file_name in files_list:
            t0 = time.time()
            res_dic[file_name] = []
            if is_cord_dim_enabled:
                res = CorDim.prepare_calculate_window_cor_dim(file_name, dimension,
                                                              cor_dim_radius, window_size, step_size)
                res_dic[file_name].append(res)
                job_index += 1
                self.update_progress(full_job, job_index)

            if is_samp_en:
                res = SampEn.prepare_calculate_window_sampen(m=dimension,
                                                             file_name=file_name,
                                                             calculation_type=en_calculation_type,
                                                             dev_coef_value=en_dev_coef_value,
                                                             use_threshold=en_use_threshold,
                                                             threshold_value=en_threshold_value,
                                                             window_size=window_size,
                                                             step_size=step_size)
                res_dic[file_name].append(res)
                job_index += 1
                self.update_progress(full_job, job_index)

            if is_ap_en:
                res = ApEn.prepare_calculate_window_apen(m=dimension,
                                                         file_name=file_name,
                                                         calculation_type=en_calculation_type,
                                                         dev_coef_value=en_dev_coef_value,
                                                         use_threshold=en_use_threshold,
                                                         threshold_value=en_threshold_value,
                                                         window_size=window_size,
                                                         step_size=step_size)
                res_dic[file_name].append(res)
                job_index += 1
                self.update_progress(full_job, job_index)

            print(time.time() - t0, "seconds per single file")
        analysis_names = ReportManager.get_analysis_types(res_dic)
        self.done.emit(','.join(analysis_names), ','.join(list(res_dic.keys())))
        ReportManager.prepare_write_report(analysis_types=analysis_names, res_dic=res_dic)

    def update_progress(self, full, current):
        progress = math.ceil((current / full) * 100)
        self.progress.emit(progress)
