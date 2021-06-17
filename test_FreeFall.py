from unittest import TestCase
import FreeFall


class Test(TestCase):

    def test_drop_calc(self):
        result = FreeFall.drop_calc(1, 1)
        self.assertAlmostEqual(result[2][-1], 14.3, 3)
