import os
from math import log

from src.core.apen import ApEn
from src.core.report import SampEnReport

from src.utils.supporting import CalculationType

__author__ = 'demidovs'


class SampEn(ApEn):
    @staticmethod
    def calculate_c(m, seq, r, n):
        assert r >= 0, 'Filtering threshold should be positive'
        similar_vectors = 0
        for i in range(0, n - m + 1):
            for j in range(0, n - m + 1):
                if r > ApEn.calculate_distance(seq[i], seq[j]):
                    similar_vectors += 1
        return similar_vectors

    @staticmethod
    def calculate_final(m, seq, r):
        # 3. Form a sequence of vectors so that
        # x[i] = [u[i],u[i+1],...,u[i+m-1]]
        # i ~ 0:N-m because indexes start from 0
        x_list = SampEn.slice_intervals(m=m, seq=seq)

        # 4. Construct the C(i,m) - portion of vectors 'similar' to i-th
        # similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
        # this is just the respective values subtraction
        return SampEn.calculate_c(m=m, seq=x_list, r=r, n=len(seq))

    @staticmethod
    def calculate_sampen(m, seq, r):
        assert m > 1, 'm value should be meaningful (> 1)'
        for_m = SampEn.calculate_final(m, seq=seq, r=r)
        if not for_m:
            return 0
        for_m_next = SampEn.calculate_final(m + 1, seq=seq, r=r)
        if not for_m_next:
            return 0
        return -log(for_m_next / for_m)

    @staticmethod
    def prepare_calculate_window_sampen(m, file_name, calculation_type, dev_coef_value, use_threshold,
                                        threshold_value, window_size=None, step_size=None):
        res_report = SampEnReport()
        res_report.set_file_name(file_name)
        res_report.set_dimension(m)
        try:
            res_report.set_window_size(window_size)
            res_report.set_step_size(step_size)
            seq_list, average_rr_list, r_val_list, window_size, step_size = SampEn.prepare_windows_calculation(m, file_name,
                                                                                                             calculation_type,
                                                                                                             dev_coef_value,
                                                                                                             use_threshold,
                                                                                                             threshold_value,
                                                                                                             window_size,
                                                                                                             step_size)
            sampen_results = [SampEn.calculate_sampen(m=m, seq=seq_list[i], r=r_val_list[i]) for i in range(len(seq_list))]
        except (ValueError, AssertionError) as e:
            res_report.set_error("Error! For file {}. Error: {}".format(file_name, e))
            return res_report

        res_report.set_avg_rr(average_rr_list)
        res_report.set_result_values(sampen_results)
        res_report.set_r_values(r_val_list)

        return res_report


if __name__ == '__main__':
    apEn = SampEn()

    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')

    # calculate for multiple windows
    r3 = apEn.prepare_calculate_window_sampen(m=2,
                                              file_name=os.path.join(data_dir, 'samp_en', '0.txt'),
                                              calculation_type=CalculationType.CONST,
                                              dev_coef_value=0.5,
                                              use_threshold=False,
                                              threshold_value=0,
                                              window_size=100,
                                              step_size=10)
    # calculate for single window
    r1 = apEn.prepare_calculate_window_sampen(m=2,
                                              file_name=os.path.join(data_dir, 'samp_en', '0.txt'),
                                              calculation_type=CalculationType.CONST,
                                              dev_coef_value=0.5,
                                              use_threshold=False,
                                              threshold_value=0)
    print(r1)
