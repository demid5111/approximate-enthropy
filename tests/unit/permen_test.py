import os
import unittest

import numpy as np
import numpy.testing as npt

from src.core.en_opt import Entropy
from src.core.permen import PermutationEntropy
from tests.unit.config_test import ConfigTest


class TestPermuteEntropySingleSequenceCalculation(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.permEn = PermutationEntropy()

    def test_calculate_permen_simple_1(self):
        data = Entropy.read_series(os.path.join(self.resource_path, 'perm_en/PermEn_simple_original.txt'),
                                   use_threshold=False, threshold_value=None)
        res = self.permEn.calculate(2, data)
        self.assertAlmostEqual(res, 0.91829, places=4, msg='incorrect PermEn')

    def test_calculate_permen_simple_2(self):
        data = Entropy.read_series(os.path.join(self.resource_path, 'perm_en/PermEn_simple_original.txt'),
                                   use_threshold=False, threshold_value=None)
        res = self.permEn.calculate(3, data)
        self.assertAlmostEqual(res, 1.52192, places=4, msg='incorrect PermEn')


class TestPermuteEntropyCollectPatterns(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.permEn = PermutationEntropy()

    def test_collect_patterns_2(self):
        data = Entropy.read_series(os.path.join(self.resource_path, 'perm_en/PermEn_simple_original.txt'),
                                   use_threshold=False, threshold_value=None)
        freqs, mapping = self.permEn.collect_pattern_frequency(data, 2)
        npt.assert_almost_equal(freqs, np.array([4 / 6, 2 / 6]), decimal=4)

    def test_collect_patterns_3(self):
        data = Entropy.read_series(os.path.join(self.resource_path, 'perm_en/PermEn_simple_original.txt'),
                                   use_threshold=False, threshold_value=None)
        freqs, mapping = self.permEn.collect_pattern_frequency(data, 3)
        npt.assert_almost_equal(freqs, np.array([2 / 5, 2 / 5, 1 / 5]), decimal=4)


class TestPermuteEntropyExtractPattern(unittest.TestCase):
    def setUp(self):
        self.permEn = PermutationEntropy()

    def test_extract_pattern_1(self):
        npt.assert_equal((0, 1, 2), self.permEn.extract_pattern(np.array([4, 7, 9])))

    def test_extract_pattern_2(self):
        npt.assert_equal((2, 0, 1), self.permEn.extract_pattern(np.array([9, 10, 6])))

    def test_extract_pattern_3(self):
        npt.assert_equal((1, 0, 2), self.permEn.extract_pattern(np.array([10, 6, 11])))

    def test_extract_pattern_4(self):
        npt.assert_equal((0, 1, 2), self.permEn.extract_pattern(np.array([-3, 0, 1])))


if __name__ == '__main__':
    unittest.main()
