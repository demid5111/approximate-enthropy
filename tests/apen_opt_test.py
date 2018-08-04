import os
import numpy as np

import unittest
from unittest.mock import patch

import src.utils.constants as constants
from src.core.apen_opt import ApEnOpt

from src.utils.supporting import CalculationType


class TestApEnOptDeviation(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEnOpt()

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
        self.apEn = ApEnOpt()

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
        self.apEn = ApEnOpt()

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

    @patch('src.core.apen_opt.ApEnOpt.calculate_apen')
    @patch('src.core.apen_opt.ApEnOpt.calculate_r')
    def test_prepare_calculate_r(self, mock_calculate_r, mock_calculate_apen):
        mock_calculate_r.return_value = 0.28237
        mock_calculate_apen.return_value = 3
        u_list = self.apEn.read_series(os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'), False, 0)
        deviation = self.apEn.calculate_deviation(u_list)
        r = self.apEn.calculate_r(CalculationType.COMPLEX, deviation, 0.5, u_list)
        self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'),
                                                CalculationType.CONST, 0, False, 0)
        self.assertEqual(mock_calculate_r.call_args[0][0], CalculationType.CONST)
        self.assertEqual(mock_calculate_r.call_args[0][1], 1.4118572032582124)
        self.assertEqual(mock_calculate_r.call_args[0][2], 0)
        np.testing.assert_array_equal(mock_calculate_r.call_args[0][3], u_list)

        self.assertEqual(mock_calculate_apen.call_args[1]['m'], 2)
        self.assertEqual(mock_calculate_apen.call_args[1]['r'], r)
        np.testing.assert_array_equal(mock_calculate_apen.call_args[1]['seq'], u_list)

        self.assertAlmostEqual(r, 0.28237, places=4, msg='incorrect r')


class TestApEnCalculateOverallApEn(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEnOpt()

    def test_calculate_apen_2_const(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'),
                                                    CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12211, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_2_dev(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'),
                                                    CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12365, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_2_complex(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_2.txt'),
                                                    CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12003, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_4_const(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                                    CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12211, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_4_dev(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                                    CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12365, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_4_complex(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_4.txt'),
                                                    CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.11040, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_10_const(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_10.txt'),
                                                    CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12211, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_10_dev(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_10.txt'),
                                                    CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.12365, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_10_complex(self):
        r = self.apEn.prepare_calculate_window_apen(2, os.path.join(constants.DATA_DIR, 'ApEn_amolituda_10.txt'),
                                                    CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.15675, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_210_const(self):
        r = self.apEn.prepare_calculate_window_apen(2,
                                                    os.path.join(constants.DATA_DIR, 'ApEn_amolituda_random_2-10.txt'),
                                                    CalculationType.CONST, 0.5,
                                                    False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.96967, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_210_dev(self):
        r = self.apEn.prepare_calculate_window_apen(2,
                                                    os.path.join(constants.DATA_DIR, 'ApEn_amolituda_random_2-10.txt'),
                                                    CalculationType.DEV, 0.5,
                                                    False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.67897, places=4, msg='incorrect ApEnOpt')

    def test_calculate_apen_210_complex(self):
        r = self.apEn.prepare_calculate_window_apen(2,
                                                    os.path.join(constants.DATA_DIR, 'ApEn_amolituda_random_2-10.txt'),
                                                    CalculationType.COMPLEX, 0.5,
                                                    False, 0)
        self.assertAlmostEqual(r.get_result_value(0), 0.26964, places=4, msg='incorrect ApEnOpt')


class TestApEnCalculateDistance(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEnOpt()

    def test_calculate_distance(self):
        a = [10, -4, 45.9]
        b = [1, 32, -0.1]
        s = self.apEn.calculate_distance(a, b)
        self.assertAlmostEqual(s, 46, places=4, msg='incorrect distance')


class TestApEnOptSlicing(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEnOpt()

    def test_slicing_ideal(self):
        a = np.array([0, 1, 10, 11, 20, 21, 30, 31, 40, 41, 50, 51])
        res = self.apEn.slice_by_window(a, 6, 2)
        exp_res = np.array([[0, 1, 10, 11, 20, 21],
                            [10, 11, 20, 21, 30, 31],
                            [20, 21, 30, 31, 40, 41],
                            [30, 31, 40, 41, 50, 51]])
        np.testing.assert_array_equal(res, exp_res)

    def test_slicing_ideal_2(self):
        a = np.array([0, 1, 10, 11, 20, 21, 30, 31, 40, 41, 50, 51])
        res = self.apEn.slice_by_window(a, 5, 3)
        exp_res = np.array([[0, 1, 10, 11, 20],
                            [11, 20, 21, 30, 31],
                            [30, 31, 40, 41, 50]])
        np.testing.assert_array_equal(res, exp_res)


class TestOptimization(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEnOpt()

    def test_calculate_c_ideal(self):
        for_m_2 = np.array([
            [10, 20],
            [20, 25],
            [25, 15],
            [15, 20],
            [20, 25],
            [25, 30]
        ])
        for_m_3 = np.array([
            [10, 20, 25],
            [20, 25, 15],
            [25, 15, 20],
            [15, 20, 25],
            [20, 25, 30]
        ])

        exp_for_m_2 = np.array([
            (1+1)/6, # (10, 20) is close to himself, (15, 20)
            (1+1+1+1)/6, # (20, 25) is close to himself, (15, 20), (20, 25), (25, 30)
            (1+0)/6, # (25, 15) is close to himself
            (1+1+1+1)/6, # (15, 20) is close to himself, (10,20), (20, 25), (20, 25)
            (1+1+1+1)/6, # (20, 25) is close to himself, (15, 20), (20, 25), (25, 30)
            (1+1+1)/6, # (25, 30) is close to himself, (20, 25), (20, 25)

        ])

        exp_for_m_3 = np.array([
            (1+1)/5, # (10, 20, 25) is close to himself, (15, 20, 25)
            (1+0)/5, # (20, 25, 15) is close to himself
            (1+0)/5, # (25, 15, 20) is close to himself
            (1+1+1)/5, # (15, 20, 25) is close to himself, (10, 20, 25), (20, 25, 30)
            (1+1)/5, # (20, 25, 30) is close to himself, (15, 20, 25)

        ])

        m_2, m_3 = self.apEn.calculate_c(for_m_2, 5)
        np.testing.assert_array_equal(m_2, exp_for_m_2)
        np.testing.assert_array_equal(m_3, exp_for_m_3)


if __name__ == '__main__':
    unittest.main()
