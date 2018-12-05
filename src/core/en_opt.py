from math import floor

import numpy as np
import pandas as pd

from src.utils.supporting import CalculationType


def fromiter(x, f):
    return np.fromiter((f(xi) for xi in x), x.dtype)


def fromiter_indexed(x, f):
    return np.fromiter((f(idx, xi) for idx, xi in np.ndenumerate(x)), x.dtype)


class RCalculator:
    @staticmethod
    def complex_r(sdds_deviation, deviation, len_seq):
        if not deviation:
            return 0
        else:
            return (-0.036 + 0.26 * (sdds_deviation / deviation) ** (1 / 2)) / ((len_seq / 1000) ** (1 / 4))

    @staticmethod
    def make_sdds(seq):
        return Entropy.calculate_deviation([seq[i] - seq[i - 1] for (i, v) in enumerate(seq[1:])])

    @staticmethod
    def calculate_r(calculation_type, r, dev_coef_value, seq):
        res_r = 0
        if calculation_type == CalculationType.CONST:
            res_r = r * 0.2
        elif calculation_type == CalculationType.DEV:
            res_r = r * dev_coef_value
        elif calculation_type == CalculationType.COMPLEX:
            res_r = RCalculator.complex_r(RCalculator.make_sdds(seq), r, len(seq))
        return res_r


class Entropy:
    report_cls = None

    @staticmethod
    def read_df(file_name, delimeter=b'.'):
        return pd.read_table(file_name,
                             sep='\n',
                             dtype=np.float64,
                             decimal=delimeter,
                             header=None)

    @staticmethod
    def read_series(file_name, use_threshold, threshold_value):
        try:
            df = Entropy.read_df(file_name)
        except ValueError:
            df = Entropy.read_df(file_name, delimeter=b',')
        res = df.values[:, 0]
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
    def calculate_deviation(seq):
        return np.std(seq)

    @staticmethod
    def calculate_deviations(x):
        return fromiter(x, Entropy.calculate_deviation)

    @staticmethod
    def calculate_averages(x, axis=1):
        return np.mean(x, axis=axis)

    @staticmethod
    def calculate_distances(calculation_type, deviations, dev_coef_value, windows):
        return fromiter_indexed(deviations,
                                lambda idx, dev: RCalculator.calculate_r(calculation_type, dev, dev_coef_value,
                                                                         windows[idx]))

    @staticmethod
    def normalize_by_min(vecs):
        # in order not to get zeros that later result in wrong bucket index
        return (vecs - np.min(vecs)) + 0.0001

    @staticmethod
    def fill_buckets(sums, r, split_factor, buckets_number):
        # compared to the paper, our buckets are intended to contain indexes
        buckets = [[] for _ in range(buckets_number)]
        indexer = Entropy.bucket_index(sums, r, split_factor)
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
    def calculate_similar_vectors(seq, r, split_factor):
        assert r >= 0, "Filtering threshold should be positive"
        number_vectors = len(seq)
        c = np.ones((number_vectors,), dtype=np.int64)
        # assuming that we have the step equals one for building sequences of vectors
        # from the original series, we always know the number of vectors for m=m+1
        c_next = np.ones((number_vectors - 1,), dtype=np.int64)

        sums = np.sum(seq, axis=1)
        sums_normalized = Entropy.normalize_by_min(sums)
        buckets_number = Entropy.bucket_index(np.max(sums_normalized), r, split_factor)
        buckets = Entropy.fill_buckets(sums_normalized, r, split_factor, buckets_number)
        buckets_sorted = Entropy.sort_inside_buckets(buckets, seq)
        deduced_m = seq[0].shape[0]
        for i_b in range(buckets_number):
            for idx, i in enumerate(buckets_sorted[i_b]):
                # compare within the bucket where the original vector is placed
                # to_compare_with = buckets_sorted[i_b][idx + 1:]
                to_compare_with = Entropy.collect_with_first_diff_less_than(seq[i][0], r, buckets_sorted[i_b][idx + 1:],
                                                                            seq)
                # then compare within neighbours
                for j_b in range(max(0, i_b - deduced_m * split_factor), i_b):
                    # to_compare_with.extend(buckets_sorted[j_b])
                    to_compare_with.extend(
                        Entropy.collect_with_first_diff_less_than(seq[i][0], r, buckets_sorted[j_b], seq))
                for j in to_compare_with:
                    if Entropy.is_similar(seq[i][1:], seq[j][1:], r):
                        c[i] += 1
                        c[j] += 1
                        # assuming that we have the step equals one
                        # and overall seq=[1,2,3,4,5,6,7,8]
                        # and for m=2 we have i=[1,2,3] compared to j=[5,6,7]
                        # and we want to check for m=3, we can take first values from next
                        # vectors: next(i)=[2,3,4], next(j)=[6,7,8]
                        if (j != len(seq) - 1 and
                                i != len(seq) - 1 and
                                Entropy.is_similar(seq[i + 1][-1:], seq[j + 1][-1:], r)):
                            c_next[i] += 1
                            c_next[j] += 1
        return c, c_next

    @staticmethod
    def prepare_windows_calculation(file_name, calculation_type, dev_coef_value, use_threshold,
                                    threshold_value, window_size=None, step_size=None):
        # 1. read the file
        u_list = Entropy.read_series(file_name, use_threshold, threshold_value)
        if not window_size:
            window_size = len(u_list)
            step_size = 1
        assert window_size <= len(u_list), "Window size can't be bigger than the size of the overall sequence"
        windows = Entropy.slice_by_window(u_list, window_size, step_size)
        max_distances = None
        if calculation_type:
            deviations = Entropy.calculate_deviations(windows)
            max_distances = Entropy.calculate_distances(calculation_type, deviations, dev_coef_value, windows)
        averages = Entropy.calculate_averages(windows)

        return windows, averages, max_distances, len(u_list)

    @staticmethod
    def calculate_similarity(m, seq, r):
        step = 1

        # 3. Form a sequence of vectors so that
        # x[i] = [u[i],u[i+1],...,u[i+m-1]]
        # i ~ 0:N-m because indexes start from 0

        # simultaneously for both m and m+1 -
        # optimization compared to the plain ApEn implementation
        m_sliced = Entropy.slice_by_window(seq, m, step)

        # 4. Construct the C(i,m) - portion of vectors "similar" to i-th
        # similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
        # this is just the respective values subtraction
        return Entropy.calculate_similar_vectors(m_sliced, r, split_factor=15)

    @staticmethod
    def calculate(m, seq, r):
        raise NotImplementedError('Each entropy type should have its own calculate method')

    @classmethod
    def prepare_calculate_windowed(cls, m, file_name,
                                   use_threshold, threshold_value,
                                   window_size=None, step_size=None,
                                   calculation_type=None, dev_coef_value=None):
        if not cls.report_cls:
            raise NotImplementedError('Any Entropy should have its own report type')
        res_report = cls.report_cls()
        res_report.set_file_name(file_name)
        res_report.set_dimension(m)
        try:
            seq_list, average_rr_list, r_val_list, seq_len = Entropy.prepare_windows_calculation(
                file_name,
                calculation_type,
                dev_coef_value,
                use_threshold,
                threshold_value,
                window_size,
                step_size)

            en_results = []
            for i in range(len(seq_list)):
                calc_kwargs = dict(m=m, seq=seq_list[i])
                if r_val_list is not None:
                    calc_kwargs['r'] = r_val_list[i]
                en_results.append(cls.calculate(**calc_kwargs))
        except (ValueError, AssertionError):
            res_report.set_error("Error! For file {}".format(file_name))
            return res_report

        res_report.set_seq_len(seq_len)
        res_report.set_window_size(window_size)
        res_report.set_step_size(step_size)
        res_report.set_avg_rr(average_rr_list)
        res_report.set_result_values(en_results)

        if r_val_list is not None:
            res_report.set_r_values(r_val_list)

        return res_report
