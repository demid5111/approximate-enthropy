import os
import unittest
from unittest.mock import MagicMock

import constants
from apen import ApEn
from supporting import CalculationType


class TestApEnDeviation(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn(m=2)

    def test_deviation1(self):
        self.apEn.read_series(os.path.join(constants.DATA_DIR,'ApEn_amolituda_2.txt'), False, 0)
        res = self.apEn.calculate_deviation(self.apEn.u_list)
        self.assertAlmostEqual(res, 1.41185, places=4, msg='incorrect deviation')

    def test_deviation2(self):
        self.apEn.read_series(os.path.join(constants.DATA_DIR,'ApEn_amolituda_4.txt'), False, 0)
        res = self.apEn.calculate_deviation(self.apEn.u_list)
        self.assertAlmostEqual(res, 2.82371, places=4, msg='incorrect deviation')

    def test_deviation3(self):
        self.apEn.read_series(os.path.join(constants.DATA_DIR,'ApEn_amolituda_10.txt'), False, 0)
        res = self.apEn.calculate_deviation(self.apEn.u_list)
        self.assertAlmostEqual(res, 7.05928, places=4, msg='incorrect deviation')

    def test_deviation4(self):
        self.apEn.read_series(os.path.join(constants.DATA_DIR,'ApEn_amolituda_random_2-10.txt'), False, 0)
        res = self.apEn.calculate_deviation(self.apEn.u_list)
        self.assertAlmostEqual(res, 4.61831, places=4, msg='incorrect deviation')


class TestApEnComplexRCalculation(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn(m=2)

    def test_sdds1(self):
        self.apEn.read_series(os.path.join(constants.DATA_DIR,'ApEn_amolituda_2.txt'), False, 0)
        sdds_deviation = self.apEn.make_sdds(self.apEn.u_list)
        self.assertAlmostEqual(sdds_deviation, 598.99675, places=4, msg='incorrect sdds')

    def test_sdds2(self):
        self.apEn.read_series(os.path.join(constants.DATA_DIR,'ApEn_amolituda_10.txt'), False, 0)
        sdds_deviation = self.apEn.make_sdds(self.apEn.u_list)
        self.assertAlmostEqual(sdds_deviation, 599.01766, places=4, msg='incorrect sdds')

    def test_complex_r_calculation1(self):
        self.apEn.read_series(os.path.join(constants.DATA_DIR,'ApEn_amolituda_2.txt'), False, 0)
        sdds_deviation = self.apEn.make_sdds(self.apEn.u_list)
        deviation = self.apEn.calculate_deviation(self.apEn.u_list)
        res = self.apEn.calculate_complex_r(sdds_deviation, deviation, len(self.apEn.u_list))
        self.assertAlmostEqual(res, 7.18754, places=4, msg='incorrect r')

    def test_complex_r_calculation2(self):
        self.apEn.read_series(os.path.join(constants.DATA_DIR,'ApEn_amolituda_10.txt'), False, 0)
        sdds_deviation = self.apEn.make_sdds(self.apEn.u_list)
        deviation = self.apEn.calculate_deviation(self.apEn.u_list)
        res = self.apEn.calculate_complex_r(sdds_deviation, deviation, len(self.apEn.u_list))
        self.assertAlmostEqual(res, 3.18753, places=4, msg='incorrect r')


class TestApEnPrepareCalculateApEn(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn(m=2)
        self.apEn.calculate_apen = MagicMock(return_value=3)

    def test_prepare_calculate_const_r(self):
        deviation = 1.41185
        self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_2.txt'), CalculationType.CONST, 0, False, 0)
        self.assertAlmostEqual(self.apEn.r, deviation * 0.2, places=4, msg='incorrect r')
        self.apEn.calculate_apen.assert_called_with(m=2)

    def test_prepare_calculate_dev_r(self):
        deviation = 1.41185
        self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_2.txt'), CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(self.apEn.r, deviation * 0.5, places=4, msg='incorrect r')
        self.apEn.calculate_apen.assert_called_with(m=2)

    def test_prepare_calculate_complex_r(self):
        self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_2.txt'), CalculationType.COMPLEX, 0, False, 0)
        self.assertAlmostEqual(self.apEn.r, 7.18754, places=4, msg='incorrect r')
        self.apEn.calculate_apen.assert_called_with(m=2)


# @unittest.skip("skipping heavy tests")
class TestApEnCalculateOverallApEn(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn(m=2)

    def test_calculate_apen_2_const(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_2.txt'), CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r, 0.12211, places=4, msg='incorrect ApEn')

    def test_calculate_apen_2_dev(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_2.txt'), CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r, 0.12365, places=4, msg='incorrect ApEn')

    def test_calculate_apen_2_complex(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_2.txt'), CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r, 0.0, places=4, msg='incorrect ApEn')

    def test_calculate_apen_4_const(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_4.txt'), CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r, 0.12211, places=4, msg='incorrect ApEn')

    def test_calculate_apen_4_dev(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_4.txt'), CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r, 0.12365, places=4, msg='incorrect ApEn')

    def test_calculate_apen_4_complex(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_4.txt'), CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r, 0.19899, places=4, msg='incorrect ApEn')

    def test_calculate_apen_10_const(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_10.txt'), CalculationType.CONST, 0.5, False, 0)
        self.assertAlmostEqual(r, 0.12211, places=4, msg='incorrect ApEn')

    def test_calculate_apen_10_dev(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_10.txt'), CalculationType.DEV, 0.5, False, 0)
        self.assertAlmostEqual(r, 0.12365, places=4, msg='incorrect ApEn')

    def test_calculate_apen_10_complex(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_10.txt'), CalculationType.COMPLEX, 0.5, False, 0)
        self.assertAlmostEqual(r, 0.12007, places=4, msg='incorrect ApEn')

    def test_calculate_apen_210_const(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_random_2-10.txt'), CalculationType.CONST, 0.5,
                                             False, 0)
        self.assertAlmostEqual(r, 0.96967, places=4, msg='incorrect ApEn')

    def test_calculate_apen_210_dev(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_random_2-10.txt'), CalculationType.DEV, 0.5,
                                             False, 0)
        self.assertAlmostEqual(r, 0.67897, places=4, msg='incorrect ApEn')

    def test_calculate_apen_210_complex(self):
        r = self.apEn.prepare_calculate_apen(2, os.path.join(constants.DATA_DIR,'ApEn_amolituda_random_2-10.txt'), CalculationType.COMPLEX, 0.5,
                                             False, 0)
        self.assertAlmostEqual(r, 0.38810, places=4, msg='incorrect ApEn')

class TestApEnCalculateDistance(unittest.TestCase):
    def setUp(self):
        self.apEn = ApEn(m=2)

    def test_calculate_distance(self):
        a = [10, -4, 45.9]
        b = [1, 32, -0.1]
        s = self.apEn.calculate_distance(a, b)
        self.assertAlmostEqual(s, 46, places=4, msg='incorrect distance')

if __name__ == '__main__':
    unittest.main()
