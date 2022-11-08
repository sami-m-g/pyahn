import os
import tempfile
import unittest

import pandas as pd
import pandas._testing as pdt

from pyahn.core import main
from pyahn.helpers import FileHelper


class TestCore(unittest.TestCase):
    def test_main(self):
        dataset = "AHN4_DTM_0.5m"
        input_data = [
            "ID,X,Y\n",
            "0,4.70754,51.9527\n",
            "1,4.88334,52.0469\n",
            "2,4.99334,52.1469\n",
            "3,4.88334,52.0469\n"
        ]
        temp_file_path = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        with open(temp_file_path, "w") as temp_file:
            temp_file.writelines(input_data)
        temp_file_path_out = temp_file_path + "_results"
        main(["-d", dataset, "-i", temp_file_path, "-o", temp_file_path_out])

        actual_z = pd.read_csv(temp_file_path_out)[FileHelper.COLUMN_KEY_Z].to_list()
        expected_z = [-1.8678573369979858, -1.6021401035789835, -1.6021401035789835,-0.061561714857816696]
        pdt.assert_almost_equal(actual_z, expected_z)


if __name__ == '__main__':
    unittest.main()