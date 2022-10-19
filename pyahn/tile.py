import argparse
import os
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
    DATA_RESOLUTION: float = 0.5
    DATA_FACTOR: int = 2
    DATA_OFFSET: int = 0

    def __init__(self, dataset: str, data_dir: str = "out", filename: str = "data.tiff"):
        self.dataset = dataset
        self.data_dir = data_dir
        self.filename = filename
        
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.data = None

        self.data_path = os.path.join(data_dir, filename)
        os.makedirs(data_dir, exist_ok=True)

    @classmethod
    def from_ahn4_array(cls, xy_coords: np.ndarray) -> 'Tile':
        _, xmin, ymin = xy_coords.min(axis=0)
        _, xmax, ymax = xy_coords.max(axis=0)
        print(f"Xmin, Ymin: ({xmin}, {ymin})\tXmax, Ymax: ({xmax}, {ymax})")
        return cls.from_ahn4_2points(xmin, ymin, xmax, ymax)

    @classmethod
    def from_ahn4_2points(cls, dataset: str, xmin: int, ymin: int, xmax: int, ymax: int) -> 'Tile':
        xmin = xmin - 1
        xmax = xmax + 1
        ymin = ymin - 1
        ymax = ymax + 1

        result = Tile(dataset)
        size_x = (xmax - xmin) * cls.DATA_FACTOR
        size_y = (ymax - ymin) * cls.DATA_FACTOR
        urllib.request.urlretrieve(
            f"{cls.URL_BASE}{dataset}/ImageServer/exportImage?bbox={xmin},{ymin},{xmax},{ymax}&bboxSR=&size={size_x},{size_y}{cls.URL_PARAMS}",
            f"{result.data_path}",
        ) # note that this might include interpolated values, check the API for the details
        result.xmin = xmin
        result.ymax = ymax
        result.data = imread(result.data_path)
        result.xmax = xmin + int(result.data.shape[1] * cls.DATA_RESOLUTION)
        result.ymin = ymax - int(result.data.shape[0] * cls.DATA_RESOLUTION)
        return result

    def get_z_for_array(self, xy_coords: np.ndarray) -> List[float]:
        z_points = []
        for row in range(xy_coords.shape[0]):
            z_points.append(self.get_z(xy_coords[row, 1], xy_coords[row, 2]))
        return z_points

    def get_z(self, x: float, y: float) -> float:
        if x < self.xmin or x > self.xmax:
            print(f"Invalid point: ({x}, {y}). X is not within: ({self.xmin}, {self.xmax})")
            return np.nan
        
        if y < self.ymin or y > self.ymax:
            print(f"Invalid point: ({x}, {y}). Y is not within: ({self.ymin}, {self.ymax})")
            return np.nan

        idx = int((x - self.xmin) / self.DATA_RESOLUTION)
        idy = int((self.ymax - y) / self.DATA_RESOLUTION)
        return self.data[idy, idx]


def main():
    parser = argparse.ArgumentParser(description="Extract Z points for XY coordinates in a csv file.")
    parser.add_argument("-d", "--dataset", help="AHN dataset to use for downloading the tile.", default="AHN4_DTM_50cm", choices=Tile.DATASETS, type=str)
    parser.add_argument("-i", "--input_file", help="Path to the csv file.", required=True, type=str)
    parser.add_argument("-o", "--output_file", help="Path to the csv file.", default="out/xyz.csv", type=str)
    args = parser.parse_args()
    
    xy_coords = np.loadtxt(args.input_file, skiprows=1, delimiter=",")

    tile = Tile.from_ahn4_array(xy_coords)
    z_coords = tile.get_z_for_array(xy_coords)
    xyz_coords = np.insert(xy_coords, 3, z_coords, axis=1)
    np.savetxt(args.output_file, xyz_coords, delimiter=",", header="ID,X,Y,Z", comments="")


if __name__ == "__main__":
    main()