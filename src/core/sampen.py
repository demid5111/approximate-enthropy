import os
from math import log

import src.utils.constants as constants
from src.core.apen import ApEn
from src.core.report import SampEnReport

from src.utils.supporting import CalculationType

__author__ = 'demidovs'


class SampEn(ApEn):
    def calculate_c(self, m, seq, r, n):
        assert r >= 0, 'Filtering threshold should be positive'
        similar_vectors = 0
        for i in range(0, n - m + 1):
            for j in range(0, n - m + 1):
                if r > self.calculate_distance(seq[i], seq[j]):
                    similar_vectors += 1
        return similar_vectors

    def calculate_final(self, m, seq, r):
        # 3. Form a sequence of vectors so that
        # x[i] = [u[i],u[i+1],...,u[i+m-1]]
        # i ~ 0:N-m because indexes start from 0
        x_list = self.slice_intervals(m=m, seq=seq)

        # 4. Construct the C(i,m) - portion of vectors 'similar' to i-th
        # similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
        # this is just the respective values subtraction
        return self.calculate_c(m=m, seq=x_list, r=r, n=len(seq))

    def calculate_sampen(self, m, seq, r):
        assert m > 1, 'm value should be meaningful (> 1)'
        for_m = self.calculate_final(m, seq=seq, r=r)
        if not for_m:
            return 0
        for_m_next = self.calculate_final(m + 1, seq=seq, r=r)
        if not for_m_next:
            return 0
        return -log(for_m_next / for_m)

    def prepare_calculate_window_sampen(self, m, file_name, calculation_type, dev_coef_value, use_threshold,
                                        threshold_value, window_size=None, step_size=None):

        seq_list, average_rr_list, r_val_list, window_size, step_size = self.prepare_windows_calculation(m, file_name,
                                                                                                         calculation_type,
                                                                                                         dev_coef_value,
                                                                                                         use_threshold,
                                                                                                         threshold_value,
                                                                                                         window_size,
                                                                                                         step_size)
        sampen_results = [self.calculate_sampen(m=m, seq=seq_list[i], r=r_val_list[i]) for i in range(len(seq_list))]

        res_report = SampEnReport()
        res_report.set_avg_rr(average_rr_list)
        res_report.set_window_size(window_size)
        res_report.set_step_size(step_size)
        res_report.set_result_values(sampen_results)
        res_report.set_r_values(r_val_list)

        return res_report


if __name__ == '__main__':
    apEn = SampEn()

    # calculate for multiple windows
    r3 = apEn.prepare_calculate_window_sampen(m=2,
                                              file_name=os.path.join(constants.DATA_DIR, 'samp_en', '0.txt'),
                                              calculation_type=CalculationType.CONST,
                                              dev_coef_value=0.5,
                                              use_threshold=False,
                                              threshold_value=0,
                                              window_size=100,
                                              step_size=10)
    # calculate for single window
    r1 = apEn.prepare_calculate_window_sampen(m=2,
                                              file_name=os.path.join(constants.DATA_DIR, 'samp_en', '0.txt'),
                                              calculation_type=CalculationType.CONST,
                                              dev_coef_value=0.5,
                                              use_threshold=False,
                                              threshold_value=0)
    print(r1)
