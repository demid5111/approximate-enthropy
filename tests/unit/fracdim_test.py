import os
import unittest

from src.core.fracdim import FracDim
from tests.unit.config_test import ConfigTest


class TestFracDimPrepareCurve(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.fracDim = FracDim()
        self.raw_series = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_prepare_curve_0(self):
        k = 1
        m = 1
        expected_series = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        res_seq = self.fracDim.prepare_curve(self.raw_series, m, k)
        self.assertListEqual(res_seq, expected_series)

    def test_prepare_curve_1(self):
        k = 2
        m = 1
        expected_series = [1, 3, 5, 7, 9]
        res_seq = self.fracDim.prepare_curve(self.raw_series, m, k)
        self.assertListEqual(res_seq, expected_series)

    def test_prepare_curve_2(self):
        k = 3
        m = 1
        expected_series = [1, 4, 7, 10]
        res_seq = self.fracDim.prepare_curve(self.raw_series, m, k)
        self.assertListEqual(res_seq, expected_series)

    def test_prepare_curve_3(self):
        k = 1
        m = 3
        expected_series = [3, 4, 5, 6, 7, 8, 9, 10]
        res_seq = self.fracDim.prepare_curve(self.raw_series, m, k)
        self.assertListEqual(res_seq, expected_series)

    def test_prepare_curve_4(self):
        k = 2
        m = 4
        expected_series = [4, 6, 8, 10]
        res_seq = self.fracDim.prepare_curve(self.raw_series, m, k)
        self.assertListEqual(res_seq, expected_series)

    def test_prepare_curve_5(self):
        k = 3
        m = 5
        expected_series = [5, 8]
        res_seq = self.fracDim.prepare_curve(self.raw_series, m, k)
        self.assertListEqual(res_seq, expected_series)


class TestFracDimCalculateCurveLength(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.fracDim = FracDim()
        self.raw_series = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_calculate_curve_length_0(self):
        k = 1
        m = 1
        series = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        N = len(self.raw_series)
        result = self.fracDim.calculate_curve_length(series, N, m, k)
        expected = 9
        self.assertEqual(result, expected)

    def test_calculate_curve_length_1(self):
        k = 2
        m = 4
        series = [4, 6, 8, 10]
        N = len(self.raw_series)
        result = self.fracDim.calculate_curve_length(series, N, m, k)
        expected = 4.5
        self.assertEqual(result, expected)

    def test_calculate_curve_length_2(self):
        k = 3
        m = 1
        series = [1, 4, 7, 10]
        N = len(self.raw_series)
        result = self.fracDim.calculate_curve_length(series, N, m, k)
        expected = 3
        self.assertEqual(result, expected)

    def test_calculate_curve_length_3(self):
        k = 3
        m = 2
        series = [2, 5, 8]
        N = len(self.raw_series)
        result = self.fracDim.calculate_curve_length(series, N, m, k)
        expected = 3
        self.assertEqual(result, expected)

    def test_calculate_curve_length_4(self):
        k = 3
        m = 3
        series = [3, 6, 9]
        N = len(self.raw_series)
        result = self.fracDim.calculate_curve_length(series, N, m, k)
        expected = 3
        self.assertEqual(result, expected)


class TestFracDimFindAverageLengthSingleK(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.fracDim = FracDim()
        self.raw_series = [10, 8, 9, 5, 4, 2, 6, 7, 3, 1, 9]

    def test_find_average_length_single_0(self):
        k = 3
        result = self.fracDim.find_average_length_single(self.raw_series, k)
        self.assertAlmostEqual(3.95061, result, places=4)


class TestFracDimFindAverageLengthMultipleK(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.fracDim = FracDim()
        self.raw_series = [10, 8, 9, 5, 4, 2, 6, 7, 3, 1, 9]

    def test_find_average_length_multi_0(self):
        max_k = 3
        result = self.fracDim.find_average_length_multi(self.raw_series, max_k)
        expected = [9.5625, 8.5, 3.45679]
        for l, r in zip(expected, result):
            self.assertAlmostEqual(l, r, places=4)


class TestFracDimCalculateSlope(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.fracDim = FracDim()

    def test_calculate_slope_0(self):
        max_k = 3
        lengths = [29.0, 8.5, 3.45679]
        result = self.fracDim.calculate_slope(lengths, max_k)
        expected = 1.91821
        self.assertAlmostEqual(expected, result, places=4)


class TestFracDimCalculateE2E(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.fracDim = FracDim()

    def test_calculate_higuchi_straight_line(self):
        max_k = 3
        series = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        result = self.fracDim.calculate_higuchi(series, max_k)
        expected = 1
        self.assertAlmostEqual(expected, result, places=4)


class TestFracDimCalculation(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.fracDim = FracDim()

    def test_deviation1(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'cosin_random_ampl_4_N_310.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=len(u_list) // 2)
        self.assertAlmostEqual(res, 1.88171, places=4, msg='incorrect frac dim')

    def test_deviation2(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'cosin_random_ampl_4_N_600.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.63519, places=4, msg='incorrect frac dim')

    def test_deviation3(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'real_data_1_N_401.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.38991, places=4, msg='incorrect frac dim')

    def test_deviation4(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'real_data_2_N_401.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.63234, places=4, msg='incorrect frac dim')

    def test_deviation5(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'real_data_3_N_345.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=len(u_list) // 2)
        self.assertAlmostEqual(res, 1.87767, places=4, msg='incorrect frac dim')

    def test_deviation6(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'real_data_4_N_334.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.47539, places=4, msg='incorrect frac dim')

    def test_deviation7(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'real_data_5_N_318.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.63094, places=4, msg='incorrect frac dim')

    def test_deviation8(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'sinus_600_ampl_2_N_300.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.87068, places=4, msg='incorrect frac dim')

    def test_deviation9(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'sinus_600_ampl_3_N_300.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.87121, places=4, msg='incorrect frac dim')

    def test_deviation10(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'sinus_ampl_4_N_304.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.87046, places=4, msg='incorrect frac dim')

    def test_deviation11(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'sinus_ampl_8_N_300.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.87068, places=4, msg='incorrect frac dim')

    def test_deviation12(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'sinus_ampl_20_N_300.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.87068, places=4, msg='incorrect frac dim')

    def test_deviation13(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'sinus_ampl_20_N_600.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.85130, places=4, msg='incorrect frac dim')

    def test_deviation14(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'sinus_ampl_rand_N_300.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.62865, places=4, msg='incorrect frac dim')

    def test_deviation15(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'sinus_ampl_random_N_300.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.77773, places=4, msg='incorrect frac dim')

    def test_deviation16(self):
        u_list = self.fracDim.read_series(os.path.join(self.resource_path, 'frac_dim', 'sinus_ampl_random_N_600.txt'),
                                          False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.77236, places=4, msg='incorrect frac dim')

    def test_deviation17(self):
        path = os.path.join(self.resource_path, 'frac_dim', 'sinus_cosinus_ampl_400_N_300.txt')
        u_list = self.fracDim.read_series(path, False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1.75188, places=4, msg='incorrect frac dim')

    def test_deviation18(self):
        path = os.path.join(self.resource_path, 'frac_dim', 'straight_line_ampl_600_N_300.txt')
        u_list = self.fracDim.read_series(path, False, 0)
        res = self.fracDim.calculate_higuchi(u_list, max_k=20)
        self.assertAlmostEqual(res, 1, places=4, msg='incorrect frac dim')


if __name__ == '__main__':
    unittest.main()
