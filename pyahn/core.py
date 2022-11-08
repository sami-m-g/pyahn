import argparse
import sys

from pyahn.helpers import EllipsisHelper, FileHelper


def main(args: list[str]) -> list[float]:
    parser = argparse.ArgumentParser(description="Extract Z points for XY coordinates in a csv file.")
    parser.add_argument(
        "-d", "--dataset", help="AHN dataset to use for getting Z points.", type=str, default="AHN4_DTM_0.5m",
        choices=EllipsisHelper.DATASETS_MAP.keys()
    )
    parser.add_argument("-i", "--input_file", help="Path to the input csv file.", type=str, required=True)
    parser.add_argument("-o", "--output_file", help="Path for the output csv file.", type=str, default="out/xyz.csv")
    pargs = parser.parse_args(args)

    xy_points = FileHelper.get_xy_points(pargs.input_file)
    z_points = EllipsisHelper.get_z_points(xy_points, pargs.dataset)
    FileHelper.save_xyz_points(xy_points, z_points, pargs.output_file)


if __name__ == "__main__":
    main(sys.argv[1:]) # pragma: no cover