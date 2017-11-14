"""
Algorithms implemented:
* Higuchi T (1988) Approach to an irregular time series on the
basis of the fractal theory. Physica D 31:277–283
*
"""
from math import floor, log

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
            seq_list, window_size, step_size = DimUtils.prepare_windows(file_name, window_size, step_size)
            fracdim_results = [FracDim.calculate_higuchi(i, max_k) for i in seq_list]
            res_report.set_window_size(window_size)
            res_report.set_step_size(step_size)
        except (ValueError, AssertionError):
            res_report.set_error("Error! For file {}".format(file_name))
            return res_report

        res_report.set_max_k(max_k)
        res_report.set_result_values(fracdim_results)

        return res_report

    @staticmethod
    def max_index(original_length, initial_time, interval_time):
        return floor((original_length - initial_time)/interval_time)

    @staticmethod
    def calculate_curve_length(curve, original_length, initial_time, interval_time):
        a = FracDim.max_index(original_length, initial_time, interval_time)
        norm_factor = (original_length - 1)/(a * interval_time)
        diffs = []
        for (index, value) in enumerate(curve):
            if index == 0:
                continue
            diff = value - curve[index-1]
            diffs.append(abs(diff))

        return sum(diffs) * norm_factor

    @staticmethod
    def prepare_curve(old_seq, initial_time, interval_time):
        assert isinstance(initial_time, int), 'Initial time should be integer'
        assert initial_time < len(old_seq), 'Initial time should be integer'
        assert isinstance(interval_time, int), 'Interval time should be integer'

        total = len(old_seq)
        res_seq = []
        step_num = 0
        while True:
            new_index = initial_time + step_num * interval_time
            step_num += 1
            if new_index >= total:
                break
            res_seq.append(old_seq[new_index])
        return res_seq

    @staticmethod
    def find_average_length_single(old_seq, interval_time):
        """
        Finds average length of the curve. For that, m (start point) is changing from 1...k(~interval_time)
        :param old_seq: sequence to base on
        :param interval_time: k - step
        :return:
        """
        lengths = []
        for m in range(interval_time):
            curve = FracDim.prepare_curve(old_seq, m, interval_time)
            res = FracDim.calculate_curve_length(curve, len(old_seq), m, interval_time)
            lengths.append(res)
        return sum(lengths)/len(lengths)

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
        for k in range(1, max_interval_time):
            avg_lengths.append(FracDim.find_average_length_single(old_seq, k))
        return avg_lengths

    @staticmethod
    def log_avg_lengths(avg_lengths):
        return [log(i) for i in avg_lengths]

    @staticmethod
    def calculate_slope(avg_lengths, max_k):
        ref = [log(1/i if i > 0 else 1) for i in range(max_k)]
        log_avg_l = FracDim.log_avg_lengths(avg_lengths)
        return LSM.calculate(list(zip(log_avg_l, ref)))[0]


if __name__ == '__main__':
    dimension = 2
    radius = 0.99

    initial_time = 3
    interval_time = 3

    old_seq = [i for i in range(100)]
    print(old_seq)

    sl = FracDim.calculate_higuchi(old_seq, 20)
    print(sl)
