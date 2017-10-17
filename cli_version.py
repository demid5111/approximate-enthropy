import argparse
from collections import OrderedDict

from src.core.apen import ApEn
from src.core.cordim import CorDim
from src.core.sampen import SampEn
from src.utils.supporting import CalculationType


class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'
    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value)


def str2bool(v):
    return True if v == "ON" else False


def prepare_parser(launch_log_dic):
    parser = argparse.ArgumentParser(description='Run cardio algorithms\n For booleans use either YES or NO', prog='cli_version.py')

    parser.add_argument('--approximate-entropy', type=str2bool, default="OFF",
                        help=launch_log_dic['approximate_entropy'])

    parser.add_argument('--sample-entropy', type=str2bool, default="OFF",
                        help=launch_log_dic['sample_entropy'])

    parser.add_argument('--correlation-dimension', type=str2bool, default="OFF",
                        help=launch_log_dic['correlation_dimension'])

    parser.add_argument('--file-name', required=True,
                        help=launch_log_dic['file_name'])

    parser.add_argument('--use-windows', required=True, type=str2bool,
                        help=launch_log_dic['use_windows'])

    parser.add_argument('--window-size', type=int,
                        help=launch_log_dic['window_size'])

    parser.add_argument('--window-step', type=int,
                        help=launch_log_dic['window_step'])

    parser.add_argument('--dimension', required=True, type=int, default=2,
                        help=launch_log_dic['dimension'])

    parser.add_argument('--entropy-use-threshold', required=True, type=str2bool,
                        help=launch_log_dic['entropy_use_threshold'])

    parser.add_argument('--entropy-threshold-value', type=int,
                        help=launch_log_dic['entropy_threshold_value'])

    parser.add_argument('--entropy-r-mode', type=str,
                        choices=['STANDARD', 'CUSTOM', 'RCHON'],
                        help=launch_log_dic['entropy_r_mode'])

    parser.add_argument('--entropy-r-coef', type=float,
                        help=launch_log_dic['entropy_r_coef'])

    parser.add_argument('--correlation-dimension-radius', type=float,
                        help=launch_log_dic['correlation_dimension_radius'])

    return parser


def prepare_description_texts():
    d = OrderedDict()
    d['approximate_entropy'] = 'Calculate Approximate Entropy'
    d['sample_entropy'] = 'Calculate Sample Entropy'
    d['correlation_dimension'] = 'Calculate Correlation Dimension'
    d['dimension'] = 'Dimension or size of vectors that we compare during analysis'
    d['use_windows'] = 'Use sliding window'
    d['window_size'] = 'Size of the sliding window'
    d['window_step'] = 'Sliding step of the window'
    d['entropy_use_threshold'] = 'Limit minimum number of RR intervals to start analysis'
    d['entropy_threshold_value'] = 'Minimum number of RR intervals to start analysis'
    d['entropy_r_mode'] = 'Calculation strategy for Entropy'
    d['entropy_r_coef'] = 'Coefficient for r calculation for Entropy'
    d['correlation_dimension_radius'] = 'Radius for correlation dimension'
    d['file_name'] = 'File containing data of RR intervals'
    return d


def print_processed_args(d, all_vars):
    for key, value in d.items():
        if not all_vars[key]:
            continue
        print(value + ': ' + str(all_vars[key]))


def check_args_combinations(parser, args):
    all_vars = vars(args)

    is_m = 'dimension' in all_vars
    if not is_m:
        parser.error('Calculation requires dimensions value')

    is_windows = 'use_windows' in all_vars and all_vars['use_windows']
    is_windows_size = 'window_size' in all_vars
    is_step_size = 'step_size' in all_vars
    is_windows_valid = not is_windows or (is_windows and (not is_windows_size or is_step_size))

    if not is_windows_valid:
        parser.error('Calculate either without windows or if using windows, specify window size and step')

    is_entropy_used = (('approximate_entropy' in all_vars and all_vars['approximate_entropy'])
                       or ('sample_entropy' in all_vars and all_vars['sample_entropy']))
    is_r_mode = 'entropy_r_mode' in all_vars and bool(all_vars['entropy_r_mode'])
    is_threshold_used = 'entropy_use_threshold' in all_vars and all_vars['entropy_use_threshold']
    threshold_value = 'entropy_threshold_value' in all_vars
    is_threshold_valid = not is_threshold_used or (is_threshold_used and threshold_value)

    if is_entropy_used and (not is_r_mode or not is_threshold_valid) and not is_r_mode:
        parser.error('Entropy requires r mode and either without threshold or with threshold value')

    is_cordim_used = 'correlation_dimension' in all_vars
    is_radius = 'correlation_dimension_radius' in all_vars

    if is_cordim_used and not is_radius:
        parser.error('Correlation dimension requires radius value')


if __name__ == '__main__':
    launch_log_dic = prepare_description_texts()

    parser = prepare_parser(launch_log_dic)
    args = parser.parse_args()

    check_args_combinations(parser, args)
    print_processed_args(launch_log_dic, vars(args))

    t = ''
    use_threshold = args.entropy_use_threshold
    if args.entropy_r_mode == 'STANDARD':
        t = CalculationType.CONST
    elif args.entropy_r_mode == 'CUSTOM':
        t = CalculationType.DEV
    elif args.entropy_r_mode == 'RCHON':
        t = CalculationType.COMPLEX
    if args.approximate_entropy:
        apEn = ApEn()
        report = apEn.prepare_calculate_window_apen(args.dimension, args.file_name, t, args.entropy_r_coef,
                                           use_threshold, args.entropy_threshold_value, args.window_size,
                                           args.window_step)
        print(report)
    if args.sample_entropy:
        apEn = SampEn()
        report = apEn.prepare_calculate_window_sampen(args.dimension, args.file_name, t, args.entropy_r_coef,
                                             use_threshold, args.entropy_threshold_value, args.window_size,
                                             args.window_step)
        print(report)
    if args.correlation_dimension:
        apEn = CorDim()
        report = apEn.prepare_calculate_window_cor_dim(args.file_name, args.dimension, args.correlation_dimension_radius,
                                              args.window_size, args.window_step)
        print(report)
