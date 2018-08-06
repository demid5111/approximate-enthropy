import time
import os

from src.core.apen import ApEn
from src.core.apen_opt import ApproximateEntropy
from src.core.sampen import SampEn
from src.core.sampen_opt import SampleEntropy

from src.utils import constants
from src.utils.supporting import CalculationType

MAX_ITER = 100


def collect_avg(f):
    opt_l = []
    for i in range(MAX_ITER):
        # print('{}/{}'.format(i + 1, MAX_ITER))
        a = time.time()
        f(10,
          os.path.join(constants.DATA_DIR, 'ApEn_amolituda_random_2-10.txt'),
          CalculationType.DEV, 0.5,
          30, 0)
        opt_l.append(time.time() - a)
    return sum(opt_l) / len(opt_l)


opt_time_a = collect_avg(ApproximateEntropy.prepare_calculate_windowed)
plain_time_a = collect_avg(ApEn.prepare_calculate_window_apen)

opt_time_s = collect_avg(SampleEntropy.prepare_calculate_windowed)
plain_time_s = collect_avg(SampEn.prepare_calculate_window_sampen)

print('Opt ApEn: {}, plain AptEn: {}. Better in {} times.'.format(opt_time_a, plain_time_a, plain_time_a / opt_time_a))
print('Opt SampEn: {}, plain SampEn: {}. Better in {} times.'.format(opt_time_s, plain_time_s, plain_time_s / opt_time_s))
