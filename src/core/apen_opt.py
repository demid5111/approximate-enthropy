"""
Optimized calculation of the ApEn.

Algorithm is well described here: http://www.mdpi.com/1099-4300/20/1/61

@article{manis2018low,
  title={Low Computational Cost for Sample Entropy},
  author={Manis, George and Aktaruzzaman, Md and Sassi, Roberto},
  journal={Entropy},
  volume={20},
  number={1},
  pages={61},
  year={2018},
  publisher={Multidisciplinary Digital Publishing Institute}
}

In particular, we have taken the bucket-based one, as it performs well on the signals of small (<1000) length

We see 3.9x speedup compared to the naive implementation
"""

import operator
import os
import numpy as np
from math import log, floor

import src.utils.constants as constants
from src.core.report import ApEnReport

from src.utils.supporting import CalculationType

__author__ = 'demidovs'


def fromiter(x, f):
    return np.fromiter((f(xi) for xi in x), x.dtype)


def fromiter_indexed(x, f):
    return np.fromiter((f(idx, xi) for idx, xi in np.ndenumerate(x)), x.dtype)


class ApEnOpt:
    @staticmethod
    def read_series(file_name, use_threshold, threshold_value):
        res = np.loadtxt(file_name, dtype=np.float64)
        if use_threshold:
            assert res.shape[0] >= threshold_value, \
                'Sample length is too small. Need more than {}'.format(str(threshold_value))
        return res

    @staticmethod
    def slice_by_window(values, window_size, step_size):
        number_of_windows = floor((values.shape[0] - window_size) / step_size) + 1
        indexer = np.arange(window_size)[None, :] + step_size * np.arange(number_of_windows)[:, None]
        return values[indexer]

    @staticmethod
    def calculate_distance(x1, x2):
        assert len(x1) == len(x2), "Vectors should be of equal sizes: " + str(x1) + " : " + str(x2)
        return max(map(abs, map(operator.sub, x1, x2)))

    @staticmethod
    def calculate_deviation(seq):
        return np.std(seq)

    @staticmethod
    def calculate_deviations(x):
        return fromiter(x, ApEnOpt.calculate_deviation)

    @staticmethod
    def calculate_averages(x, axis=1):
        return np.mean(x, axis=axis)

    @staticmethod
    def is_dissimilar_pair(a, b, threshold):
        return np.abs(a - b) > threshold

    @staticmethod
    def calculate_distances(calculation_type, deviations, dev_coef_value, windows):
        return fromiter_indexed(deviations,
                                lambda idx, dev: ApEnOpt.calculate_r(calculation_type, dev, dev_coef_value,
                                                                     windows[idx]))

    @staticmethod
    def calculate_complex_r(sdds_deviation, deviation, len_seq):
        if not deviation:
            return 0
        else:
            return (-0.036 + 0.26 * (sdds_deviation / deviation) ** (1 / 2)) / ((len_seq / 1000) ** (1 / 4))

    @staticmethod
    def normalize_by_min(vecs):
        return vecs - np.min(vecs)

    @staticmethod
    def fill_buckets(sums, r, split_factor, buckets_number):
        # compared to the paper, our buckets are intended to contain indexes
        buckets = [[] for _ in range(buckets_number)]
        indexer = ApEnOpt.bucket_index(sums, r, split_factor)
        for idx, val in np.ndenumerate(indexer):
            i = idx[0]
            value = val - 1
            buckets[value].append(i)
        return buckets

    @staticmethod
    def bucket_index(point, r, split_factor):
        return np.ceil(point / r / split_factor).astype('int')

    @staticmethod
    def sort_inside_buckets(buckets, seq):
        return [sorted(b, key=lambda idx: seq[idx][0]) for b in buckets]

    @staticmethod
    def is_similar(vec1, vec2, threshold):
        for idx, val in np.ndenumerate(vec1):
            if np.abs(val - vec2[idx]) > threshold:
                return False
        return True

    @staticmethod
    def collect_with_first_diff_less_than(val, threshold, bucket, seq):
        first = next((idx for idx, i in enumerate(bucket) if abs(seq[i][0] - val) <= threshold), None)
        if first is None:
            return []
        second = next((idx for idx, i in enumerate(bucket) if abs(seq[i][0] - val) > threshold and idx > first), None)
        return bucket[first:second]

    @staticmethod
    def calculate_c(seq, r, split_factor):
        assert r >= 0, "Filtering threshold should be positive"
        number_vectors = len(seq)
        c = np.ones((number_vectors,), dtype=np.int64)
        # assuming that we have the step equals one for building sequences of vectors
        # from the original series, we always know the number of vectors for m=m+1
        c_next = np.ones((number_vectors - 1,), dtype=np.int64)

        sums = np.sum(seq, axis=1)
        sums_normalized = ApEnOpt.normalize_by_min(sums)
        buckets_number = ApEnOpt.bucket_index(np.max(sums_normalized), r, split_factor)
        buckets = ApEnOpt.fill_buckets(sums_normalized, r, split_factor, buckets_number)
        buckets_sorted = ApEnOpt.sort_inside_buckets(buckets, seq)
        deduced_m = seq[0].shape[0]
        for i_b in range(buckets_number):
            for idx, i in enumerate(buckets_sorted[i_b]):
                # compare within the bucket where the original vector is placed
                # to_compare_with = buckets_sorted[i_b][idx + 1:]
                to_compare_with = ApEnOpt.collect_with_first_diff_less_than(seq[i][0], r, buckets_sorted[i_b][idx + 1:],
                                                                            seq)
                # then compare within neighbours
                for j_b in range(max(0, i_b - deduced_m * split_factor), i_b):
                    # to_compare_with.extend(buckets_sorted[j_b])
                    to_compare_with.extend(
                        ApEnOpt.collect_with_first_diff_less_than(seq[i][0], r, buckets_sorted[j_b], seq))
                for j in to_compare_with:
                    if ApEnOpt.is_similar(seq[i], seq[j], r):
                        c[i] += 1
                        c[j] += 1
                        # assuming that we have the step equals one
                        # and overall seq=[1,2,3,4,5,6,7,8]
                        # and for m=2 we have i=[1,2,3] compared to j=[5,6,7]
                        # and we want to check for m=3, we can take first values from next
                        # vectors: next(i)=[2,3,4], next(j)=[6,7,8]
                        if (j != len(seq) - 1 and
                                i != len(seq) - 1 and
                                r >= ApEnOpt.calculate_distance(seq[i + 1][-1:], seq[j + 1][-1:])):
                            c_next[i] += 1
                            c_next[j] += 1
        c_avg = c / number_vectors
        c_next_avg = c_next / (number_vectors - 1)
        return c_avg, c_next_avg

    @staticmethod
    def calculate_phi(c_avg, c_avg_next):
        c_avg_log = np.log(c_avg)
        c_avg_next = np.log(c_avg_next)

        phi = ApEnOpt.calculate_averages(c_avg_log, axis=0)
        phi_next = ApEnOpt.calculate_averages(c_avg_next, axis=0)

        return phi, phi_next

    @staticmethod
    def calculate_apen(m, seq, r):
        step = 1
        m_next = m + 1

        # 3. Form a sequence of vectors so that
        # x[i] = [u[i],u[i+1],...,u[i+m-1]]
        # i ~ 0:N-m because indexes start from 0

        # simultaneously for both m and m+1 -
        # optimization compared to the plain ApEn implementation
        m_sliced = ApEnOpt.slice_by_window(seq, m, step)

        # 4. Construct the C(i,m) - portion of vectors "similar" to i-th
        # similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
        # this is just the respective values subtraction
        c_avg, c_avg_next = ApEnOpt.calculate_c(m_sliced, r, split_factor=15)

        phi, phi_next = ApEnOpt.calculate_phi(c_avg, c_avg_next)

        return phi - phi_next

    @staticmethod
    def make_sdds(seq):
        return ApEnOpt.calculate_deviation([seq[i] - seq[i - 1] for (i, v) in enumerate(seq[1:])])

    @staticmethod
    def calculate_r(calculation_type, r, dev_coef_value, seq):
        res_r = 0
        if calculation_type == CalculationType.CONST:
            res_r = r * 0.2
        elif calculation_type == CalculationType.DEV:
            res_r = r * dev_coef_value
        elif calculation_type == CalculationType.COMPLEX:
            res_r = ApEnOpt.calculate_complex_r(ApEnOpt.make_sdds(seq), r, len(seq))
        return res_r

    @staticmethod
    def prepare_calculate_window_apen(m, file_name, calculation_type, dev_coef_value, use_threshold,
                                      threshold_value, window_size=None, step_size=None):
        res_report = ApEnReport()
        res_report.set_file_name(file_name)
        res_report.set_dimension(m)
        try:
            seq_list, average_rr_list, r_val_list, window_size, step_size = ApEnOpt.prepare_windows_calculation(m,
                                                                                                                file_name,
                                                                                                                calculation_type,
                                                                                                                dev_coef_value,
                                                                                                                use_threshold,
                                                                                                                threshold_value,
                                                                                                                window_size,
                                                                                                                step_size)
            apen_results = [ApEnOpt.calculate_apen(m=m, seq=seq_list[i], r=r_val_list[i]) for i in range(len(seq_list))]
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
        u_list = ApEnOpt.read_series(file_name, use_threshold, threshold_value)
        if not window_size:
            window_size = len(u_list)
            step_size = 1
        assert window_size <= len(u_list), "Window size can't be bigger than the size of the overall sequence"
        windows = ApEnOpt.slice_by_window(u_list, window_size, step_size)
        deviations = ApEnOpt.calculate_deviations(windows)
        max_distances = ApEnOpt.calculate_distances(calculation_type, deviations, dev_coef_value, windows)
        averages = ApEnOpt.calculate_averages(windows)

        return windows, averages, max_distances, window_size, step_size


if __name__ == "__main__":
    apEn = ApEnOpt()

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
