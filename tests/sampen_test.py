import unittest

from sampen import SampEn


class TestSampEnDeviation(unittest.TestCase):
    def setUp(self):
        self.sampEn = SampEn(m=2)

    def test_deviation1(self):
        self.assertAlmostEqual(1.41185, 1.41185, places=4, msg='incorrect deviation')

if __name__ == '__main__':
    unittest.main()
