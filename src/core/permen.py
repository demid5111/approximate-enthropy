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
        return tuple(np.argsort(seq))

    @staticmethod
    def collect_pattern_frequency(seq, size):
        patterns = []
        counts = []
        num_elements = len(seq) - size + 1
        for idx in range(num_elements):
            current_pattern = PermutationEntropy.extract_pattern(seq[idx:idx + size])
            try:
                position = patterns.index(current_pattern)
            except ValueError:
                patterns.append(current_pattern)
                counts.append(1)
            else:
                counts[position] += 1
        return np.array(counts) / num_elements, np.array(patterns)

    @staticmethod
    def calculate(m, seq, r=None):
        frequences, mapping = PermutationEntropy.collect_pattern_frequency(seq, m)
        return -1 * np.dot(frequences, np.log2(frequences))
