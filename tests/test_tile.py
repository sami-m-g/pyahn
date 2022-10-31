import os
import tempfile
import unittest

import numpy as np

from pyahn.tile import Tile, main as tile_main


class TestTileHelper(unittest.TestCase):
    def test_tile_main(self):
        input_data = [
            "ID,X,Y\n",
            "0,131178.7,476558.84\n",
            "1,131178.47,476558.79\n",
            "2,131178.76,476559.03\n",
            "3,131179.02,476558.98\n"
        ]
        temp_file_path = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        with open(temp_file_path, "w") as temp_file:
            temp_file.writelines(input_data)

        expected_z = [-0.0228, 0.0572, 0.1372, -0.1028]
        actual_z = tile_main(["-d", "AHN4_DTM_50cm", "-i", temp_file_path, "-o", temp_file_path + "_results"])
        self.assertEqual(actual_z, expected_z)
    
    def test_tile_get_z_out_of_bound_points(self):
        tile = Tile.from_ahn_2points("AHN4_DTM_50cm", 131000, 476400, 131300, 476750)

        self.assertTrue(tile.get_z(130000, 476558.84) is np.nan)
        self.assertTrue(tile.get_z(131178.47, 476751) is np.nan)


if __name__ == '__main__':
    unittest.main()