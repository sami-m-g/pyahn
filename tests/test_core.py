"""Tests for core module."""
import os
import tempfile

import pandas as pd
import pandas._testing as pdt

from pyahn.core import main
from pyahn.helpers import FileHelper


def test_main():
    """Gets Z points almost equal to expected."""
    dataset = "AHN4_DTM_0.5m"
    input_data = [
        "ID,X,Y\n",
        "0,4.70754,51.9527\n",
        "1,4.88334,52.0469\n",
        "2,4.99334,52.1469\n",
        "3,4.88334,52.0469\n"
    ]
    temp_file_path = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    with open(temp_file_path, "w", encoding="utf-8") as temp_file:
        temp_file.writelines(input_data)
    temp_file_path_out = temp_file_path + "_results"
    main(["-d", dataset, "-i", temp_file_path, "-o", temp_file_path_out])

    actual_z = pd.read_csv(temp_file_path_out)[FileHelper.COLUMN_KEY_Z].to_list()
    expected_z = [0.0, 0.0, 0.0, 0.0]
    pdt.assert_almost_equal(actual_z, expected_z)
