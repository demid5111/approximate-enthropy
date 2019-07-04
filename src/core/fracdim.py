"""
Algorithms implemented:
* Higuchi T (1988) Approach to an irregular time series on the
basis of the fractal theory. Physica D 31:277–283
*
"""
import math
from math import log, ceil

from src.core.apen import ApEn
from src.core.dim_utils import DimUtils
from src.core.lsm import LSM
from src.core.report import FracDimReport


class FracDim(ApEn):
    @staticmethod
    def calculate_higuchi(old_seq, max_k):
        l = FracDim.find_average_length_multi(old_seq, max_k)
        sl = FracDim.calculate_slope(l, max_k)
        return sl

    @staticmethod
    def prepare_calculate_window_frac_dim(file_name, max_k, window_size, step_size):
        res_report = FracDimReport()
        res_report.set_file_name(file_name)

        try:
            seq_list, window_size, step_size, seq_len = DimUtils.prepare_windows(file_name, window_size, step_size)
            fracdim_results = [FracDim.calculate_higuchi(i, max_k) for i in seq_list]
            res_report.set_window_size(window_size)
            res_report.set_step_size(step_size)
        except (ValueError, AssertionError):
            res_report.set_error("Error! For file {}".format(file_name))
            return res_report

        res_report.set_max_k(max_k)
        res_report.set_result_values(fracdim_results)
        res_report.set_seq_len(seq_len)

        return res_report

    @staticmethod
    def max_index(original_length, initial_time, interval_time):
        res = (original_length - initial_time) / interval_time
        return ceil(res) if (float(res) % 1) >= 0.5 else round(res)

    @staticmethod
    def calculate_curve_length(curve, original_length, initial_time, interval_time):
        a = (original_length - initial_time) // interval_time
        norm_factor = (original_length - 1) / (a * interval_time)
        diffs = []
        for (index, value) in enumerate(curve):
            if index == 0:
                continue
            diff = value - curve[index - 1]
            diffs.append(abs(diff))

        return sum(diffs) * norm_factor * (1 / interval_time)

    @staticmethod
    def prepare_curve(old_seq, initial_time, interval_time):
        assert isinstance(initial_time, int), 'Initial time should be integer'
        assert initial_time < len(old_seq), 'Initial time should be integer'
        assert isinstance(interval_time, int), 'Interval time should be integer'

        return old_seq[initial_time - 1::interval_time]

    @staticmethod
    def find_average_length_single(old_seq, interval_time):
        """
        Finds average length of the curve. For that, m (start point) is changing from 1...k(~interval_time)
        :param old_seq: sequence to base on
        :param interval_time: k - step
        :return:
        """
        lengths = []
        for m in range(1, interval_time + 1):
            curve = FracDim.prepare_curve(old_seq, m, interval_time)
            res = FracDim.calculate_curve_length(curve, len(old_seq), m, interval_time)
            lengths.append(res)
        return sum(lengths) / interval_time

    @staticmethod
    def find_average_length_multi(old_seq, max_interval_time):
        """
        Finds average lengths of all possible curves.
        For that, k (interval step) is changing from 1...max_k(~max_interval_time)
        :param old_seq: sequence to base on
        :param max_interval_time: maximum possible step
        :return:
        """
        avg_lengths = []
        for k in range(2, max_interval_time + 1):
            avg_lengths.append(FracDim.find_average_length_single(old_seq, k))
        return avg_lengths

    @staticmethod
    def log_avg_lengths(avg_lengths):
        return [log(i) if i else 1 for i in avg_lengths]

    @staticmethod
    def calculate_slope(avg_lengths, max_k):
        ref = [log(1 / i) for i in range(1, max_k+1)]
        if all(map(lambda x: x == 0, avg_lengths)):
            return 1
        log_avg_l = FracDim.log_avg_lengths(avg_lengths)
        return LSM.calculate(list(zip(ref, log_avg_l)))


if __name__ == '__main__':
    dimension = 2
    radius = 0.99

    initial_time = 3
    interval_time = 3

    old_seq = [i for i in range(100)]
    print(old_seq)

    sl = FracDim.calculate_higuchi(old_seq, 20)
    print(sl)
