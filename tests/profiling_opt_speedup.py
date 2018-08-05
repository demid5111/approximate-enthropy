import time
import os

from src.core.apen import ApEn
from src.core.apen_opt import ApEnOpt

from src.utils import constants
from src.utils.supporting import CalculationType

MAX_ITER = 100


def collect_avg(f):
    opt_l = []
    for i in range(MAX_ITER):
        print('{}/{}'.format(i + 1, MAX_ITER))
        a = time.time()
        f(10,
          os.path.join(constants.DATA_DIR, 'ApEn_amolituda_random_2-10.txt'),
          CalculationType.DEV, 0.5,
          30, 0)
        opt_l.append(time.time() - a)
    return sum(opt_l) / len(opt_l)


opt_time = collect_avg(ApEnOpt.prepare_calculate_window_apen)
plain_time = collect_avg(ApEn.prepare_calculate_window_apen)

print('Opt: {}, plain: {}. Better in {} times.'.format(opt_time, plain_time, plain_time/opt_time))
