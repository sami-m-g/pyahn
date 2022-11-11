import ellipsis as el
import geopandas as gpd
import pandas as pd
from shapely import geometry

from pyahn.model import DatasetIds


class EllipsisHelper:
    DOWNSAMPLE_WIDTH: int = 1000
    DOWNSAMPLE_HEIGHT: int = 1000
    KEY_DOWNSAMPLE_RASTER: str = "raster"
    KEY_GDF_GEOMETRY: str = "geometry"
    ELLIPSIS_CRS: str = "EPSG:4326"
    INTERPOLATION_KIND: str = "linear"

    # You can find relevant ids by going to this link: https://app.ellipsis-drive.com/drive/me?pathId=8d73b2b1-e1b0-4ec6-85e2-e53f7a580332
    # Open the folder containing the desired AHN version, then open the context menu of the item you wish to use and choose integrate
    # In the integrate dialog you can copy paste the needed pathId and timestampId
    DATASETS_MAP: dict[str, DatasetIds] = {
        "AHN3": DatasetIds("2bd5477a-8526-485f-ada8-b377f53073b0", "44d7a218-4b99-4307-8f92-cff5e328cf65"),
        "AHN3_DSM_0.5m": DatasetIds("94037eea-4196-48db-9f83-0ef330a7655e", "e6b6cc8c-998b-4715-8f39-1e0c9bf4abbe"),
        "AHN3_DSM_5m": DatasetIds("284e07d0-dd71-439a-bde4-70f8c302d008", "86a147bd-ef79-4f0d-af62-43812f79d1cb"),
        "AHN3_DTM_0.5m": DatasetIds("69f81443-c000-4479-b08f-2078e3570394", "eac8dc12-07ad-4fce-8509-705ccd46423f"),
        "AHN3_DTM_5m": DatasetIds("c9d96854-419e-4d95-8d14-835d8ab941d7", "db5f3f83-1b9e-4306-8a2b-531d06a392f2"),
        "AHN4_DSM_0.5m": DatasetIds("78080fff-8bcb-4258-bb43-be9de956b3e0", "988569a7-2180-4ac2-9f39-d471105fc38d"),
        "AHN4_DSM_5m": DatasetIds("73e91774-b6bb-4f57-ba49-2e0b1a68e71a", "46113b06-670d-47b3-b837-c997113577cb"),
        "AHN4_DTM_0.5m": DatasetIds("8b60a159-42ed-480c-ba86-7f181dcf4b8a", "597aed16-09e3-467b-b3c6-a47967956fd3"),
        "AHN4_DTM_5m": DatasetIds("fd0410f9-8922-45da-a815-bafda0c58b6f", "e8a3972b-85b6-4848-8e08-2da7a8c94072")
    }

    @staticmethod
    def change_crs(line: list[list[float]], from_crs: str, to_crs: str) -> list[float]:
        line_sh = geometry.LineString(line)
        line_gdf = gpd.GeoDataFrame({EllipsisHelper.KEY_GDF_GEOMETRY: [line_sh]})
        line_gdf.crs = from_crs
        line_gdf = line_gdf.to_crs(to_crs)
        return line_gdf[EllipsisHelper.KEY_GDF_GEOMETRY].values[0]

    @staticmethod
    def get_z_points(xy_points: pd.DataFrame, dataset: str, input_crs: str  = "EPSG:28992") -> list[float]:
        # Get xy_points_line from dataframe
        dataset_ids = EllipsisHelper.DATASETS_MAP[dataset]
        x_points = xy_points[FileHelper.COLUMN_KEY_X].to_list()
        y_points = xy_points[FileHelper.COLUMN_KEY_Y].to_list()
        xy_points_line = [[x_points[i], y_points[i]] for i in range(len(xy_points))]

        # Convert from RDNAP to WGS84
        line_el = EllipsisHelper.change_crs(xy_points_line, input_crs, EllipsisHelper.ELLIPSIS_CRS)

        values = el.path.raster.timestamp.getValuesAlongLine(
            pathId=dataset_ids.path_id, timestampId=dataset_ids.time_stamp_id, line=line_el
        )
        return [value[0] for value in values]


class FileHelper:
    COLUMN_KEY_X: str = "X"
    COLUMN_KEY_Y: str = "Y"
    COLUMN_KEY_Z: str = "Z"

    @staticmethod
    def get_xy_points(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    @staticmethod
    def save_xyz_points(xy_points: pd.DataFrame, z_points: list[float], file_path: str) -> None:
        z_column = pd.Series(z_points)
        columns_len = len(xy_points.columns)
        xy_points.insert(loc=columns_len, column=FileHelper.COLUMN_KEY_Z, value=z_column)
        xy_points.to_csv(file_path)