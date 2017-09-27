import unittest
from unittest.mock import patch

from cordim import CorDim


class TestCorDimCalculateHeviside(unittest.TestCase):
    def setUp(self):
        self.corDim = CorDim()

    def test_calc_heviside_0(self):
        r = self.corDim.calc_heviside(10, 20)
        self.assertEqual(0, r, msg='heviside equals 0 for all negative differences')

    def test_calc_heviside_1(self):
        r = self.corDim.calc_heviside(20, 10)
        self.assertEqual(1, r, msg='heviside equals 1 for all positive differences')

    def test_calc_heviside_2(self):
        r = self.corDim.calc_heviside(-10, -11)
        self.assertEqual(1, r, msg='heviside equals 1 for all positive differences')

    def test_calc_heviside_3(self):
        r = self.corDim.calc_heviside(-10, -1)
        self.assertEqual(0, r, msg='heviside equals 0 for all negative differences')


class TestCorDimCalculateAttractor(unittest.TestCase):
    def setUp(self):
        self.corDim = CorDim()

    def test_calc_attractor_0(self):
        r = self.corDim.calc_attractor(10, 20)
        self.assertAlmostEqual(0.76862, r, places=4, msg='normal attractor fails')

    def test_calc_attractor_1(self):
        r = self.corDim.calc_attractor(0, 20)
        self.assertAlmostEqual(0.3338, r, places=4, msg='attractor for zero cor func')

    def test_calc_attractor_2(self):
        r = self.corDim.calc_attractor(10, 0)
        self.assertAlmostEqual(2.3026, r, places=4, msg='attractor for zero radius')

    def test_calc_attractor_3(self):
        r = self.corDim.calc_attractor(0, 0)
        self.assertEqual(1, r, msg='attractor for zero radius and zero cor func')


class TestCorDimCalculateCor(unittest.TestCase):
    def setUp(self):
        self.corDim = CorDim()

    @patch('apen.ApEn.calculate_distance')
    @patch('cordim.CorDim.calc_heviside')
    def test_calc_cor_func_0(self, mock_cordim_calc_haviside, mock_apen_calc_distance):
        mock_apen_calc_distance.return_value = 0.3
        mock_cordim_calc_haviside.return_value=0.4
        r = self.corDim.calc_cor_func([600,], 5)
        mock_apen_calc_distance.assert_called_with(600, 600)
        mock_cordim_calc_haviside.assert_called_with(5, 0.3)
        self.assertAlmostEqual(0.4, r, places=4, msg='calc cor fails for normal case')

    @patch('apen.ApEn.calculate_distance')
    @patch('cordim.CorDim.calc_heviside')
    def test_calc_cor_func_1(self, mock_cordim_calc_haviside, mock_apen_calc_distance):
        r = self.corDim.calc_cor_func([], 5)
        self.assertEqual(0, r, msg='calc cor fails for empty sequence')


if __name__ == '__main__':
    unittest.main()
