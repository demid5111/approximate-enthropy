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
        self.assertAlmostEqual(3.45679, result, places=4)


class TestFracDimFindAverageLengthMultipleK(unittest.TestCase, ConfigTest):
    def setUp(self):
        self.fracDim = FracDim()
        self.raw_series = [10, 8, 9, 5, 4, 2, 6, 7, 3, 1, 9]

    def test_find_average_length_multi_0(self):
        max_k = 3
        result = self.fracDim.find_average_length_multi(self.raw_series, max_k)
        expected = [29.0, 8.5, 3.45679]
        for l,r in zip(expected, result):
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

if __name__ == '__main__':
    unittest.main()
