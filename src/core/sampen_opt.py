from src.core.en_opt import Entropy
from src.core.report import SampEnReport
import numpy as np


class SampleEntropy(Entropy):
    report_cls = SampEnReport

    @staticmethod
    def calculate(m, seq, r):
        c_avg, c_avg_next = Entropy.calculate_similarity(m, seq, r, include_self_check=False)
        return SampleEntropy.calculate_psi(c_avg, c_avg_next)

    @staticmethod
    def calculate_psi(c_avg, c_avg_next):
        avg_prob = np.sum(c_avg)
        avg_prob_next = np.sum(c_avg_next)

        return -np.log(avg_prob_next/avg_prob) if avg_prob > 0 and avg_prob_next > 0 else 0

