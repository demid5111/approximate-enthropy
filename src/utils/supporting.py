import os
import sys


class CalculationType:
    COMPLEX = 3
    DEV = 2
    CONST = 1


class AnalysisType:
    AP_EN = 'ApEn'
    SAMP_EN = 'SampEn'
    PERM_EN = 'PermEn'
    COR_DIM = 'CorDim'
    FRAC_DIM = 'FracDim'


ARTIFACTS_DIR = (os.path.expanduser('~/Documents/HeartAlgo-Analyzer-Artifacts')
                 if sys.platform == 'darwin' else '.')
