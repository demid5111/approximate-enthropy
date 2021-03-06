"""
This is the implementation of the original paper:

@article{bandt2002permutation,
  title={Permutation entropy: a natural complexity measure for time series},
  author={Bandt, Christoph and Pompe, Bernd},
  journal={Physical review letters},
  volume={88},
  number={17},
  pages={174102},
  year={2002},
  publisher={APS}
}
"""
import numpy as np

from src.core.en_opt import Entropy
from src.core.report import PermutationEntropyReport


class PermutationEntropy(Entropy):
    report_cls = PermutationEntropyReport

    @staticmethod
    def extract_pattern(seq):
        """
        Extraction happens due to the following rule:
        if the sequence contains repeating elements then all repeating elements get
        the same rank (order number). For example:
        [5,4,-1,5] is reflected as a pattern [2,1,0,2]

        This is implemented according to:

        @article{bian2012modified,
          title={Modified permutation-entropy analysis of heartbeat dynamics},
          author={Bian, Chunhua and Qin, Chang and Ma, Qianli DY and Shen, Qinghong},
          journal={Physical Review E},
          volume={85},
          number={2},
          pages={021906},
          year={2012},
          publisher={APS}
        }

        :param seq: sequence with numbers
        :return: a tuple with indexes
        """
        res = tuple(np.argsort(seq))
        if len(set(seq)) == len(seq):
            return res

        # there are duplicates
        value_to_id = {}
        new_id = 0
        for el in sorted(seq):
            try:
                value_to_id[el]
            except KeyError:
                value_to_id[el] = new_id
                new_id += 1
            else:
                pass
        return tuple(value_to_id[el] for el in seq)

    @staticmethod
    def collect_pattern_frequency(seq, size, stride):
        patterns = []
        counts = []
        stride = 1 if stride is None else stride
        for idx in range(len(seq)):
            i = idx
            acc_seq = []
            while True:
                acc_seq.append(seq[i])
                i += stride
                if i >= len(seq) or len(acc_seq) == size:
                    break
            if len(acc_seq) != size:
                break

            current_pattern = PermutationEntropy.extract_pattern(acc_seq)
            try:
                position = patterns.index(current_pattern)
            except ValueError:
                patterns.append(current_pattern)
                counts.append(1)
            else:
                counts[position] += 1
        return np.array(counts) / sum(counts), np.array(patterns)

    @staticmethod
    def calculate(m, seq, stride):
        frequences, mapping = PermutationEntropy.collect_pattern_frequency(seq, m, stride)
        return -1 * np.dot(frequences, np.log2(frequences))

    @staticmethod
    def normalize_series(series, n):
        """
        calculating h small
        :return: normalized series
        """
        return np.array(series) * (1 / (n - 1))

    @classmethod
    def prepare_calculate_windowed(cls, m, file_name,
                                   use_threshold, threshold_value,
                                   window_size=None, step_size=None,
                                   calculation_type=None, dev_coef_value=None,
                                   normalize=False, stride_size=None):
        if not cls.report_cls:
            raise NotImplementedError('Any Entropy should have its own report type')
        res_report = cls.report_cls()
        res_report.set_file_name(file_name)
        res_report.set_dimension(m)
        try:
            seq_list, average_rr_list, r_val_list, seq_len = Entropy.prepare_windows_calculation(
                file_name,
                calculation_type=calculation_type,
                dev_coef_value=dev_coef_value,
                use_threshold=use_threshold,
                threshold_value=threshold_value,
                window_size=window_size,
                step_size=step_size)

            en_results = []
            for i in range(len(seq_list)):
                calc_kwargs = dict(m=m, seq=seq_list[i], stride=stride_size)
                en_results.append(cls.calculate(**calc_kwargs))
        except (ValueError, AssertionError):
            res_report.set_error("Error! For file {}".format(file_name))
            return res_report

        res_report.set_seq_len(seq_len)
        res_report.set_window_size(window_size)
        res_report.set_step_size(step_size)
        res_report.set_avg_rr(average_rr_list)
        res_report.set_result_values(en_results)
        res_report.set_stride_value(1 if stride_size is None else stride_size)
        if normalize:
            res_report.set_normalized_values(PermutationEntropy.normalize_series(en_results, m))

        return res_report
