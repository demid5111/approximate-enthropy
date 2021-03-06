from math import log, floor

from src.core.dim_utils import DimUtils
from src.core.apen import ApEn
from src.core.report import CorDimReport


class CorDim(ApEn):
    @staticmethod
    def calc_heviside(radius, diff):
        return 0 if radius - diff < 0 else 1

    @staticmethod
    def calc_cor_func(seq, radius):
        res = []
        for i in seq:
            for j in seq:
                res.append(CorDim.calc_heviside(radius, ApEn.calculate_distance(i, j)))
        coef = 1 / (len(seq) ** 2) if len(seq) > 0 else 1
        return coef * sum(res)

    @staticmethod
    def calc_attractor(cor_func_res, radius):
        cor_val = log(cor_func_res) if cor_func_res != 0 else 1
        radius_val = log(radius) if radius != 0 and radius != 1 else 1
        return cor_val / radius_val

    @staticmethod
    def calculate_cor_dim(u_list, dimension, radius):
        portrait = CorDim.slice_intervals(dimension, u_list)
        res = CorDim.calc_cor_func(portrait, radius)
        return CorDim.calc_attractor(res, radius)

    @staticmethod
    def prepare_calculate_window_cor_dim(file_name, dimension, radius, window_size, step_size):
        res_report = CorDimReport()
        res_report.set_file_name(file_name)
        res_report.set_dimension(dimension)

        try:
            seq_list, window_size, step_size, seq_len = DimUtils.prepare_windows(file_name, window_size, step_size)
            cordim_results = [CorDim.calculate_cor_dim(i, dimension, radius) for i in seq_list]
            res_report.set_window_size(window_size)
            res_report.set_step_size(step_size)
        except (ValueError, AssertionError):
            res_report.set_error("Error! For file {}".format(file_name))
            return res_report

        res_report.set_radius(radius)
        res_report.set_result_values(cordim_results)
        res_report.set_seq_len(seq_len)

        return res_report


if __name__ == '__main__':
    dimension = 2
    radius = 0.99

    corDim = CorDim()
    seq = CorDim.read_series('data/ApEn_amolituda_2.txt', False, False)
    portrait = CorDim.slice_intervals(dimension, seq)
    res = CorDim.calc_cor_func(portrait, radius)
    attractor = CorDim.calc_attractor(res, radius)
    print(attractor)
