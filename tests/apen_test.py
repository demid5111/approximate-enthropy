import os
import unittest
from unittest.mock import patch

import src.utils.constants as constants
from src.core.apen import ApEn

from src.utils.supporting import CalculationType


class TestApEnDeviation(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn()

    def test_deviation1(self):
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'), False, 0)
        res = self.apEn.calculate_deviation(u_list)
        self.assertAlmostEqual(res, 1.41185, places=4, msg='incorrect deviation')

    def test_deviation2(self):
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'), False, 0)
        res = self.apEn.calculate_deviation(u_list)
        self.assertAlmostEqual(res, 2.82371, places=4, msg='incorrect deviation')

    def test_deviation3(self):
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_10.txt'), False, 0)
        res = self.apEn.calculate_deviation(u_list)
        self.assertAlmostEqual(res, 7.05928, places=4, msg='incorrect deviation')

    def test_deviation4(self):
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_random_2-10.txt'), False, 0)
        res = self.apEn.calculate_deviation(u_list)
        self.assertAlmostEqual(res, 4.61831, places=4, msg='incorrect deviation')


class TestApEnComplexRCalculation(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn()

    def test_sdds1(self):
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'), False, 0)
        sdds_deviation = self.apEn.make_sdds(u_list)
        self.assertAlmostEqual(sdds_deviation, 1.35532, places=4, msg='incorrect sdds')

    def test_sdds2(self):
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_10.txt'), False, 0)
        sdds_deviation = self.apEn.make_sdds(u_list)
        self.assertAlmostEqual(sdds_deviation, 6.77663, places=4, msg='incorrect sdds')

    def test_complex_r_calculation1(self):
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'), False, 0)
        sdds_deviation = self.apEn.make_sdds(u_list)
        deviation = self.apEn.calculate_deviation(u_list)
        res = self.apEn.calculate_complex_r(sdds_deviation, deviation, len(u_list))
        self.assertAlmostEqual(res, 0.29556, places=4, msg='incorrect r')

    def test_complex_r_calculation2(self):
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_10.txt'), False, 0)
        sdds_deviation = self.apEn.make_sdds(u_list)
        deviation = self.apEn.calculate_deviation(u_list)
        res = self.apEn.calculate_complex_r(sdds_deviation, deviation, len(u_list))
        self.assertAlmostEqual(res, 0.29556, places=4, msg='incorrect r')


class TestApEnPrepareCalculateApEn(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn()

    def test_prepare_calculate_const_r(self):
        deviation = 1.41185
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'), False, 0)
        r = self.apEn.calculate_r(CalculationType.CONST, deviation, 0, u_list)
        self.assertAlmostEqual(r, deviation * 0.2, places=4, msg='incorrect r')

    def test_prepare_calculate_dev_r(self):
        deviation = 1.41185
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'), False, 0)
        r = self.apEn.calculate_r(CalculationType.DEV, deviation, 0.5, u_list)
        self.assertAlmostEqual(r, deviation * 0.5, places=4, msg='incorrect r')

    def test_prepare_calculate_complex_r(self):
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'), False, 0)
        deviation = self.apEn.calculate_deviation(u_list)
        r = self.apEn.calculate_r(CalculationType.COMPLEX, deviation, 0.5, u_list)
        self.assertAlmostEqual(r, 0.29556, places=4, msg='incorrect r')

    @patch('src.core.apen.ApEn.calculate_apen')
    @patch('src.core.apen.ApEn.calculate_r')
    def test_prepare_calculate_r(self, mock_calculate_r, mock_calculate_apen):
        mock_calculate_r.return_value = 0.28237
        mock_calculate_apen.return_value=3
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'), False, 0)
        deviation = self.apEn.calculate_deviation(u_list)
        r = self.apEn.calculate_r(CalculationType.COMPLEX, deviation, 0.5, u_list)
        self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'),
                                                CalculationType.CONST, 0, False, 0)
        mock_calculate_r.assert_called_with(CalculationType.CONST, 1.4118572032582122, 0, u_list)
        mock_calculate_apen.assert_called_with(m=2, r=r, seq=u_list)
        self.assertAlmostEqual(r, 0.28237, places=4, msg='incorrect r')


class TestApEnCalculateOverallApEn(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn()

    def test_calculate_apen_2_const(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'),
                                                    CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12211, places=4, msg='incorrect ApEn')

    def test_calculate_apen_2_dev(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'),
                                                    CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12365, places=4, msg='incorrect ApEn')

    def test_calculate_apen_2_complex(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'),
                                                    CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12003, places=4, msg='incorrect ApEn')

    def test_calculate_apen_4_const(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                                    CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12211, places=4, msg='incorrect ApEn')

    def test_calculate_apen_4_dev(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                                    CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12365, places=4, msg='incorrect ApEn')

    def test_calculate_apen_4_complex(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                                    CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.11040, places=4, msg='incorrect ApEn')

    def test_calculate_apen_10_const(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_10.txt'),
                                                    CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12211, places=4, msg='incorrect ApEn')

    def test_calculate_apen_10_dev(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_10.txt'),
                                                    CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12365, places=4, msg='incorrect ApEn')

    def test_calculate_apen_10_complex(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_10.txt'),
                                                    CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.15675, places=4, msg='incorrect ApEn')

    def test_calculate_apen_210_const(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_random_2-10.txt'),
                                                    CalculationType.CONST, 0.5,
                                                    False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.96967, places=4, msg='incorrect ApEn')

    def test_calculate_apen_210_dev(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_random_2-10.txt'),
                                                    CalculationType.DEV, 0.5,
                                                    False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.67897, places=4, msg='incorrect ApEn')

    def test_calculate_apen_210_complex(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_random_2-10.txt'),
                                                    CalculationType.COMPLEX, 0.5,
                                                    False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.26964, places=4, msg='incorrect ApEn')


class TestApEnCalculateDistance(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn()

    def test_calculate_distance(self):
        a = [10, -4, 45.9]
        b = [1, 32, -0.1]
        s = self.apEn.calculate_distance(a, b)
        self.assertAlmostEqual(s, 46, places=4, msg='incorrect distance')


if __name__ == '__main__':
    unittest.main()
