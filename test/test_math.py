import unittest
from WonderPy.util import wwMath


class MyTestCase(unittest.TestCase):

    def test_coordinate_conversion(self):
        d = wwMath.coords_api_to_json_tilt(3.0)
        self.assertAlmostEqual(d, -3.0)

        d = wwMath.coords_api_to_json_pan(3.0)
        self.assertAlmostEqual(d,  3.0)

        x, y = wwMath.coords_api_to_json_pos(1.0, 2.0)
        self.assertAlmostEqual(x,  2.0)
        self.assertAlmostEqual(y, -1.0)

        d = wwMath.coords_json_to_api_tilt(3.0)
        self.assertAlmostEqual(d, -3.0)

        d = wwMath.coords_json_to_api_pan(3.0)
        self.assertAlmostEqual(d,  3.0)

        x, y = wwMath.coords_json_to_api_pos(1.0, 2.0)
        self.assertAlmostEqual(x, -2.0)
        self.assertAlmostEqual(y,  1.0)


if __name__ == '__main__':
    unittest.main()
