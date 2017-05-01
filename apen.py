import operator
import os
from math import log, floor

import constants
from supporting import CalculationType

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
    def get_result_val(d):
        return d['result']

    @staticmethod
    def get_avg_rr_val(d):
        return d['average_rr']

    @staticmethod
    def get_r_val(d):
        return d['r']

    @staticmethod
    def get_n_val(d):
        return d['n']

    @staticmethod
    def get_step_size_val(d):
        return d['step_size']

    @staticmethod
    def get_err_val(d):
        return d['error']

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

    def calculate_c(self, m, seq, r, n):
        c_list = []
        assert r >= 0, "Filtering threshold should be positive"
        for i in range(n - m + 1):
            similar_vectors = 0
            for j in range(n - m + 1):
                if r > self.calculate_distance(seq[i], seq[j]):
                    similar_vectors += 1
            c_list.append(similar_vectors / (n - m + 1))
        return c_list

    def _final(self, m, c_list, n):
        res = [log(c_list[i]) if c_list[i] else 0.0 for i in range(n - m + 1)]
        return sum(res) * ((n - m + 1) ** (-1))

    def calculate_final(self, m, seq, r):
        # 3. Form a sequence of vectors so that
        # x[i] = [u[i],u[i+1],...,u[i+m-1]]
        # i ~ 0:N-m because indexes start from 0
        x_list = self.slice_intervals(m=m, seq=seq)

        # 4. Construct the C(i,m) - portion of vectors "similar" to i-th
        # similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
        # this is just the respective values subtraction
        c_list = self.calculate_c(m=m, seq=x_list, r=r, n=len(seq))

        return self._final(m=m, c_list=c_list, n=len(seq))

    def calculate_apen(self, m, seq, r):
        return self.calculate_final(m, seq=seq, r=r) - self.calculate_final(m + 1, seq=seq, r=r)

    def make_sdds(self, seq):
        return self.calculate_deviation([seq[i] - seq[i - 1] for (i, v) in enumerate(seq[1:])])

    def calculate_r(self, calculation_type, r, dev_coef_value, seq):
        res_r = 0
        if calculation_type == CalculationType.CONST:
            res_r = r * 0.2
        elif calculation_type == CalculationType.DEV:
            res_r = r * dev_coef_value
        elif calculation_type == CalculationType.COMPLEX:
            res_r = self.calculate_complex_r(self.make_sdds(seq), r, len(seq))
        return res_r

    def prepare_calculate_window_apen(self, m, file_name, calculation_type, dev_coef_value, use_threshold,
                                      threshold_value, window_size=None, step_size=None):

        seq_list, average_rr_list, r_val_list, window_size, step_size = self.prepare_windows_calculation(m, file_name,
                                                                                                         calculation_type,
                                                                                                         dev_coef_value,
                                                                                                         use_threshold,
                                                                                                         threshold_value,
                                                                                                         window_size,
                                                                                                         step_size)
        apen_results = [self.calculate_apen(m=m, seq=seq_list[i], r=r_val_list[i]) for i in range(len(seq_list))]

        return {
            'result': apen_results,
            'average_rr': average_rr_list,
            'r': r_val_list,
            'n': window_size,
            'step_size': step_size,
        }

    def prepare_windows_calculation(self, m, file_name, calculation_type, dev_coef_value, use_threshold,
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
            r_val = self.calculate_r(calculation_type, deviation, dev_coef_value, new_seq)
            r_val_list.append(r_val)
            average_rr_list.append(self.get_average_rr(seq=new_seq))
            seq_list.append(new_seq)
        return seq_list, average_rr_list, r_val_list, window_size, step_size


def make_report(file_name="results/results.csv", res_dic=None, is_ap_en=True):
    if not res_dic:
        print("Error in generating report")
    with open(file_name, "w") as f:
        f.write('Entropy type, {}\n'.format('Approximate Entropy' if is_ap_en else 'Sample Entropy'))

        # get sample size of window and step
        any_key = list(res_dic.keys())[0]
        f.write('Window size, {}\n'.format(ApEn.get_n_val(res_dic[any_key])))
        f.write('Step size, {}\n'.format(ApEn.get_step_size_val(res_dic[any_key])))

        f.write(','.join(['File name', 'Window number', 'Entropy', 'R', 'Average RR']) + '\n')

        for (file_name, ind_result) in res_dic.items():
            try:
                ApEn.get_err_val(ind_result)
                f.write(','.join([file_name, ApEn.get_err_val(ind_result)]) + '\n')
                continue
            except KeyError:
                pass
            for (window_index, res_val) in enumerate(ApEn.get_result_val(ind_result)):
                res_list = ['{}'.format(file_name),  # empty for filename column
                            str(window_index),
                            str('{0:.10f}'.format(res_val)),
                            str(ApEn.get_r_val(ind_result)[window_index]),
                            str(ApEn.get_avg_rr_val(ind_result)[window_index])]
                f.write(','.join(res_list) + '\n')


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
