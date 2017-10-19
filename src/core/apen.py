import operator
import os
from math import log, floor

import src.utils.constants as constants
from src.core.report import ApEnReport

from src.utils.supporting import CalculationType

__author__ = 'demidovs'


class ApEn:
    @staticmethod
    def read_series(file_name, use_threshold, threshold_value):
        u_list = []
        with open(file_name, "r") as f:
            for val in f.readlines():
                u_list.append(float(val.strip().replace(',', '.')))
        assert u_list, 'File is either missed or corrupted'
        if use_threshold:
            assert len(u_list) >= threshold_value, \
                'Sample length is too small. Need more than {}'.format(str(threshold_value))
        return u_list

    @staticmethod
    def slice_intervals(m, seq):
        return [seq[i:i + m] for i in range(len(seq) - m + 1)]

    @staticmethod
    def get_average_rr(seq):
        return float(sum(seq)) / len(seq)

    @staticmethod
    def calculate_distance(x1, x2):
        assert len(x1) == len(x2), "Vectors should be of equal sizes: " + str(x1) + " : " + str(x2)
        return max(map(abs, map(operator.sub, x1, x2)))

    @staticmethod
    def calculate_deviation(seq):
        total_sum_norm = sum(seq) / len(seq)
        return (sum([(i - total_sum_norm) ** 2 for i in seq]) / len(seq)) ** (1 / 2)

    @staticmethod
    def calculate_complex_r(sdds_deviation, deviation, len_seq):
        if not deviation:
            return 0
        else:
            return (-0.036 + 0.26 * (sdds_deviation / deviation) ** (1 / 2)) / ((len_seq / 1000) ** (1 / 4))

    @staticmethod
    def calculate_c(m, seq, r, n):
        c_list = []
        assert r >= 0, "Filtering threshold should be positive"
        for i in range(n - m + 1):
            similar_vectors = 0
            for j in range(n - m + 1):
                if r > ApEn.calculate_distance(seq[i], seq[j]):
                    similar_vectors += 1
            c_list.append(similar_vectors / (n - m + 1))
        return c_list

    @staticmethod
    def _final(m, c_list, n):
        res = [log(c_list[i]) if c_list[i] else 0.0 for i in range(n - m + 1)]
        return sum(res) * ((n - m + 1) ** (-1))

    @staticmethod
    def calculate_final(m, seq, r):
        # 3. Form a sequence of vectors so that
        # x[i] = [u[i],u[i+1],...,u[i+m-1]]
        # i ~ 0:N-m because indexes start from 0
        x_list = ApEn.slice_intervals(m=m, seq=seq)

        # 4. Construct the C(i,m) - portion of vectors "similar" to i-th
        # similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
        # this is just the respective values subtraction
        c_list = ApEn.calculate_c(m=m, seq=x_list, r=r, n=len(seq))

        return ApEn._final(m=m, c_list=c_list, n=len(seq))

    @staticmethod
    def calculate_apen(m, seq, r):
        return ApEn.calculate_final(m, seq=seq, r=r) - ApEn.calculate_final(m + 1, seq=seq, r=r)

    @staticmethod
    def make_sdds(seq):
        return ApEn.calculate_deviation([seq[i] - seq[i - 1] for (i, v) in enumerate(seq[1:])])

    @staticmethod
    def calculate_r(calculation_type, r, dev_coef_value, seq):
        res_r = 0
        if calculation_type == CalculationType.CONST:
            res_r = r * 0.2
        elif calculation_type == CalculationType.DEV:
            res_r = r * dev_coef_value
        elif calculation_type == CalculationType.COMPLEX:
            res_r = ApEn.calculate_complex_r(ApEn.make_sdds(seq), r, len(seq))
        return res_r

    @staticmethod
    def prepare_calculate_window_apen(m, file_name, calculation_type, dev_coef_value, use_threshold,
                                      threshold_value, window_size=None, step_size=None):
        res_report = ApEnReport()
        res_report.set_file_name(file_name)
        res_report.set_dimension(m)
        try:
            seq_list, average_rr_list, r_val_list, window_size, step_size = ApEn.prepare_windows_calculation(m, file_name,
                                                                                                             calculation_type,
                                                                                                             dev_coef_value,
                                                                                                             use_threshold,
                                                                                                             threshold_value,
                                                                                                             window_size,
                                                                                                             step_size)
            apen_results = [ApEn.calculate_apen(m=m, seq=seq_list[i], r=r_val_list[i]) for i in range(len(seq_list))]
            res_report.set_window_size(window_size)
            res_report.set_step_size(step_size)
        except (ValueError, AssertionError):
            res_report.set_error("Error! For file {}".format(file_name))
            return res_report

        res_report.set_avg_rr(average_rr_list)
        res_report.set_result_values(apen_results)
        res_report.set_r_values(r_val_list)

        return res_report

    @staticmethod
    def prepare_windows_calculation(m, file_name, calculation_type, dev_coef_value, use_threshold,
                                    threshold_value, window_size=None, step_size=None):
        # 1. read the file
        u_list = ApEn.read_series(file_name, use_threshold, threshold_value)
        if not window_size:
            window_size = len(u_list)
            step_size = 1
        assert window_size <= len(u_list), "Window size can't be bigger than the size of the overall sequence"
        r_val_list = []
        average_rr_list = []
        seq_list = []
        for current_step in range(floor((len(u_list) - window_size) / step_size) + 1):
            next_max = current_step * step_size + window_size
            if next_max > len(u_list):
                break
            new_seq = u_list[current_step * step_size:next_max]
            deviation = ApEn.calculate_deviation(new_seq)
            r_val = ApEn.calculate_r(calculation_type, deviation, dev_coef_value, new_seq)
            r_val_list.append(r_val)
            average_rr_list.append(ApEn.get_average_rr(seq=new_seq))
            seq_list.append(new_seq)
        return seq_list, average_rr_list, r_val_list, window_size, step_size


if __name__ == "__main__":
    apEn = ApEn()

    # calculate for multiple windows
    r3 = apEn.prepare_calculate_window_apen(m=2,
                                            file_name=os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                            calculation_type=CalculationType.CONST,
                                            dev_coef_value=0.5,
                                            use_threshold=False,
                                            threshold_value=0,
                                            window_size=100,
                                            step_size=10)
    # calculate for single window
    r1 = apEn.prepare_calculate_window_apen(m=2,
                                            file_name=os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                            calculation_type=CalculationType.CONST,
                                            dev_coef_value=0.5,
                                            use_threshold=False,
                                            threshold_value=0)
    print(r1)
