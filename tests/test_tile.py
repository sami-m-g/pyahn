import unittest

from pyahn.tile import Tile


class TestTileHelper(unittest.TestCase):
    def test_list_int(self):
        tile = Tile.from_ahn4_2points(131000, 476400, 131300, 476750)

        self.assertEqual(round(tile.get_z(131178.7, 476558.84), 4), -0.0228)
        self.assertEqual(round(tile.get_z(131178.47, 476558.79), 4), 0.0572)
        self.assertEqual(round(tile.get_z(131178.76, 476559.03), 4), 0.1372)
        self.assertEqual(round(tile.get_z(131179.02, 476558.98), 4), -0.1028)


if __name__ == '__main__':
    unittest.main()