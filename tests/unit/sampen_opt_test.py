import os
import unittest

from src.core.sampen_opt import SampleEntropy

from src.utils.supporting import CalculationType
from tests.unit.config_test import ConfigTest


class TestSampEnCalculateOverallSampEn(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.apEn = SampleEntropy()

    def test_calculate_sampen_0_const(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '0.txt'),
                                                 calculation_type=CalculationType.CONST,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.02061, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_0_dev(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '0.txt'),
                                                 calculation_type=CalculationType.DEV,
                                                 dev_coef_value=0.7,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.02061, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_0_complex(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '0.txt'),
                                                 calculation_type=CalculationType.COMPLEX,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.02061, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_1_const(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '1.txt'),
                                                 calculation_type=CalculationType.CONST,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.16353, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_1_dev(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '1.txt'),
                                                 calculation_type=CalculationType.DEV,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.20067, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_1_complex(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '1.txt'),
                                                 calculation_type=CalculationType.COMPLEX,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.18526, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_2_const(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '2.txt'),
                                                 calculation_type=CalculationType.CONST,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.17022, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_2_dev(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '2.txt'),
                                                 calculation_type=CalculationType.DEV,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.18628, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_2_complex(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '2.txt'),
                                                 calculation_type=CalculationType.COMPLEX,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.18603, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_3_const(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '3.txt'),
                                                 calculation_type=CalculationType.CONST,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.34032, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_3_dev(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '3.txt'),
                                                 calculation_type=CalculationType.DEV,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0.33647, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_3_complex(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '3.txt'),
                                                 calculation_type=CalculationType.COMPLEX,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0., places=4, msg='incorrect SampEn')

    def test_calculate_sampen_4_const(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '4.txt'),
                                                 calculation_type=CalculationType.CONST,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 2.63905, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_4_dev(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '4.txt'),
                                                 calculation_type=CalculationType.DEV,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 1.37486, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_4_complex(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en', '4.txt'),
                                                 calculation_type=CalculationType.COMPLEX,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0., places=4, msg='incorrect SampEn')

    def test_calculate_sampen_apsamp_const(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en',
                                                                        'ApEn_SampEn.txt'),
                                                 calculation_type=CalculationType.CONST,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 2.29666, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_apsamp_dev(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en',
                                                                        'ApEn_SampEn.txt'),
                                                 calculation_type=CalculationType.DEV,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 1.29771, places=4, msg='incorrect SampEn')

    def test_calculate_sampen_apsamp_complex(self):
        r = self.apEn.prepare_calculate_windowed(m=2,
                                                 file_name=os.path.join(self.resource_path, 'samp_en',
                                                                        'ApEn_SampEn.txt'),
                                                 calculation_type=CalculationType.COMPLEX,
                                                 dev_coef_value=0.5,
                                                 use_threshold=False,
                                                 threshold_value=0)
        self.assertAlmostEqual(r.get_result_value(0), 0., places=4, msg='incorrect SampEn')


if __name__ == '__main__':
    unittest.main()
