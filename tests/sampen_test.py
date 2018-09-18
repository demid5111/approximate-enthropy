import os
import unittest

from src.core.sampen import SampEn

from src.utils.supporting import CalculationType


# @unittest.skip("skipping heavy tests")
from tests.config_test import ConfigTest


class TestSampEnCalculateOverallSampEn(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.apEn = SampEn()

    def test_calculate_sampen_0_const(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '0.txt'),
                                                      CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.02040, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_0_dev(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '0.txt'),
                                                      CalculationType.DEV, 0.7, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.02040, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_0_complex(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '0.txt'),
                                                      CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.02040, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_1_const(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '1.txt'),
                                                      CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.13480, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_1_dev(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '1.txt'),
                                                      CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.18518, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_1_complex(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '1.txt'),
                                                      CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.17236, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_2_const(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '2.txt'),
                                                      CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.13994, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_2_dev(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '2.txt'),
                                                      CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.17185, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_2_complex(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '2.txt'),
                                                      CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.17721, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_3_const(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '3.txt'),
                                                      CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.16571, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_3_dev(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '3.txt'),
                                                      CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.29717, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_3_complex(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '3.txt'),
                                                      CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.01015, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_4_const(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '4.txt'),
                                                      CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.56509, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_4_dev(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '4.txt'),
                                                      CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 1.06521, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_4_complex(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', '4.txt'),
                                                      CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.01015, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_apsamp_const(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', 'ApEn_SampEn.txt'),
                                                      CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 1.75633, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_apsamp_dev(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', 'ApEn_SampEn.txt'),
                                                      CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 1.26286, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_apsamp_complex(self):
        r = self.apEn.prepare_calculate_window_sampen(2, os.path.join(self.resource_path, 'samp_en', 'ApEn_SampEn.txt'),
                                                      CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.10184, places=4, msg='incorrect SampEn')


if __name__ == '__main__':
    unittest.main()
