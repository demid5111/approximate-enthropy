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

    def prepare_calculate_apen(self, m, file_name, calculation_type, dev_coef_value, use_threshold, threshold_value):
        u_list = self.read_series(file_name, use_threshold, threshold_value)
        deviation = self.calculate_deviation(u_list)
        r = self.calculate_r(calculation_type, deviation, dev_coef_value, u_list)
        return {
            'result': self.calculate_apen(m=m, seq=u_list, r=r),
            'average_rr': self.get_average_rr(seq=u_list),
            'r': r,
            'n': len(u_list)
        }

    def prepare_calculate_window_apen(self, m, file_name, calculation_type, dev_coef_value, use_threshold,
                                      threshold_value, window_size, step_size):
        # 1. read the file
        u_list = ApEn.read_series(file_name, use_threshold, threshold_value)
        # 2. r is different for every window
        assert window_size <= len(u_list), "Window size can't be bigger than the size of the overall sequence"
        apen_results = []
        r_val_list = []
        for current_step in range(floor((len(u_list) - window_size) / step_size) + 1):
            next_max = current_step * step_size + window_size
            if next_max > len(u_list):
                break
            new_seq = u_list[current_step * step_size:next_max]
            deviation = ApEn.calculate_deviation(new_seq)
            r_val = self.calculate_r(calculation_type, deviation, dev_coef_value, new_seq)
            r_val_list.append(r_val)
            apen_results.append(self.calculate_apen(m=m, seq=new_seq, r=r_val))

        return apen_results


def make_report(file_name="results/results.csv", files_list=None, ap_en_list=None, r_list=None, n_list=None,
                avg_rr_list=None,
                is_ap_en=True):
    if not files_list:
        print("Error in generating report")
    with open(file_name, "w") as f:
        if is_ap_en:
            type = 'Approximate Enthropy'
        else:
            type = 'Sample Enthropy'
        f.write(','.join(['File name', type, 'R', 'N', 'Average RR']) + '\n')
        for index, name in enumerate(files_list):
            res_list = ['"{}"'.format(name),
                        str(ap_en_list[index]),
                        str(r_list[index]) if r_list else '',
                        str(n_list[index]) if n_list else '',
                        str(avg_rr_list[index]) if avg_rr_list else '']
            f.write(','.join(res_list) + '\n')


if __name__ == "__main__":
    apEn = ApEn()

    r = apEn.prepare_calculate_window_apen(m=2,
                                           file_name=os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                           calculation_type=CalculationType.CONST,
                                           dev_coef_value=0.5,
                                           use_threshold=False,
                                           threshold_value=0,
                                           window_size=100,
                                           step_size=10)
    print(r)
