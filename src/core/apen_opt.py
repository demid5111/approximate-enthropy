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

import os
import numpy as np

import src.utils.constants as constants
from src.core.en_opt import Entropy
from src.core.report import ApEnReport

from src.utils.supporting import CalculationType

__author__ = 'demidovs'


class ApEnOpt(Entropy):
    report_cls = ApEnReport

    @staticmethod
    def calculate_phi(c_avg, c_avg_next):
        c_avg_log = np.log(c_avg)
        c_avg_next = np.log(c_avg_next)

        phi = Entropy.calculate_averages(c_avg_log, axis=0)
        phi_next = Entropy.calculate_averages(c_avg_next, axis=0)

        return phi, phi_next

    @staticmethod
    def calculate(m, seq, r):
        c_avg, c_avg_next = Entropy.calculate_probabilities(m, seq, r)

        phi, phi_next = ApEnOpt.calculate_phi(c_avg, c_avg_next)

        return phi - phi_next


if __name__ == "__main__":
    apEn = ApEnOpt()

    # calculate for multiple windows
    r3 = apEn.prepare_calculate_windowed(m=2,
                                         file_name=os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                         calculation_type=CalculationType.CONST,
                                         dev_coef_value=0.5,
                                         use_threshold=False,
                                         threshold_value=0,
                                         window_size=100,
                                         step_size=10)
    # calculate for single window
    r1 = apEn.prepare_calculate_windowed(m=2,
                                         file_name=os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                         calculation_type=CalculationType.CONST,
                                         dev_coef_value=0.5,
                                         use_threshold=False,
                                         threshold_value=0)
    print(r1)
