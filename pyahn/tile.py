import argparse
import math
import os
import sys
import urllib.request
from typing import List

import numpy as np
from tifffile import imread


class Tile:
    DATASETS: List[str] = [
        "AHN3_5m",
        "AHN3_i",
        "AHN3_r",
        "AHN4_DSM_50cm",
        "AHN4_DSM_5m",
        "AHN4_DTM_50cm",
        "AHN4_DTM_5m"
    ]

    URL_BASE: str = "https://ahn.arcgisonline.nl/arcgis/rest/services/Hoogtebestand/"
    URL_PARAMS: str = "&imageSR=&time=&format=tiff&pixelType=F64&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&mosaicRule=&renderingRule=&f=image"
    DATA_FACTOR: int = 2
    OUTPUT_DIR = "out"

    def __init__(self, dataset: str, xmin: int, ymax: int, data: np.ndarray):
        self.dataset = dataset
        self.xmin = xmin
        self.ymax = ymax
        self.data = data
        if self.dataset == "AHN3_5m" or self.dataset == "AHN4_DSM_5m" or self.dataset == "AHN4_DTM_5m":
            self.resolution = 5
        else:
            self.resolution = 0.5
        self.xmax = xmin + int(data.shape[1] * self.resolution)
        self.ymin = ymax - int(data.shape[0] * self.resolution)

    @classmethod
    def from_ahn_array(cls, dataset: str, xy_coords: np.ndarray) -> 'Tile':
        _, xmin, ymin = xy_coords.min(axis=0)
        _, xmax, ymax = xy_coords.max(axis=0)
        print(f"Xmin, Ymin: ({xmin}, {ymin})\tXmax, Ymax: ({xmax}, {ymax})")
        return cls.from_ahn_2points(dataset, math.floor(xmin), math.floor(ymin), math.ceil(xmax), math.ceil(ymax))

    @classmethod
    def from_ahn_2points(cls, dataset: str, xmin: int, ymin: int, xmax: int, ymax: int) -> 'Tile':
        os.makedirs(Tile.OUTPUT_DIR, exist_ok=True)
        data_path = os.path.join(Tile.OUTPUT_DIR, f"data_{xmin}_{ymin}-{xmax}_{ymax}.tiff")

        size_x = (xmax - xmin) * cls.DATA_FACTOR
        size_y = (ymax - ymin) * cls.DATA_FACTOR
        urllib.request.urlretrieve(
            f"{cls.URL_BASE}{dataset}/ImageServer/exportImage?bbox={xmin},{ymin},{xmax},{ymax}&bboxSR=&size={size_x},{size_y}{cls.URL_PARAMS}",
            data_path,
        ) # note that this might include interpolated values, check the API for the details

        data = imread(data_path)
        return Tile(dataset, xmin, ymax, data)

    @classmethod
    def get_z_for_file(cls, dataset: str, input_file: str, output_file: str) -> List[float]:
        xy_coords = np.loadtxt(input_file, skiprows=1, delimiter=",")
        tile = Tile.from_ahn_array(dataset, xy_coords)

        z_points = []
        for row in range(xy_coords.shape[0]):
            z_points.append(tile.get_z(xy_coords[row, 1], xy_coords[row, 2]))

        xyz_coords = np.insert(xy_coords, 3, z_points, axis=1)
        np.savetxt(output_file, xyz_coords, delimiter=",", header="ID,X,Y,Z", comments="")

        return z_points

    def get_z(self, x: float, y: float) -> float:
        if x < self.xmin or x > self.xmax:
            print(f"Invalid point: ({x}, {y}). X is not within: ({self.xmin}, {self.xmax})")
            return np.nan
        
        if y < self.ymin or y > self.ymax:
            print(f"Invalid point: ({x}, {y}). Y is not within: ({self.ymin}, {self.ymax})")
            return np.nan

        idx = int((x - self.xmin) / self.resolution)
        idy = int((self.ymax - y) / self.resolution)
        return round(self.data[idy, idx], 4)


def main(args: List[str]) -> List[float]:
    parser = argparse.ArgumentParser(description="Extract Z points for XY coordinates in a csv file.")
    parser.add_argument("-d", "--dataset", help="AHN dataset to use for downloading the tile.", default="AHN4_DTM_50cm", choices=Tile.DATASETS, type=str)
    parser.add_argument("-i", "--input_file", help="Path to the csv file.", required=True, type=str)
    parser.add_argument("-o", "--output_file", help="Path to the csv file.", default="out/xyz.csv", type=str)
    args = parser.parse_args(args)

    return Tile.get_z_for_file(args.dataset, args.input_file, args.output_file)


if __name__ == "__main__":
    main(sys.argv[1:]) # pragma: no cover