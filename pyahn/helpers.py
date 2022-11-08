import ellipsis as el
import pandas as pd
from scipy import interpolate

from pyahn.model import DatasetIds


class EllipsisHelper:
    DOWNSAMPLE_WIDTH: int = 1000
    DOWNSAMPLE_HEIGHT: int = 1000
    DOWNSAMPLE_EPSG: int = 4326
    DOWNSAMPLE_RASTER_KEY: str = "raster"
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
    def get_z_points(xy_points: pd.DataFrame, dataset: str) -> list[float]:
        dataset_ids = EllipsisHelper.DATASETS_MAP[dataset]
        x_points = xy_points[FileHelper.COLUMN_KEY_X].to_list()
        y_points = xy_points[FileHelper.COLUMN_KEY_Y].to_list()

        # The first action is to cacluate a bounding box for the raster we need to retrieve
        x_min = min(x_points)
        x_max = max(x_points)
        y_min = min(y_points)
        y_max = max(y_points)

        # Now we retrieve the needed raster we use epsg = 4326 but we can use other coordinates as well
        extent = {"xMin": x_min, "xMax": x_max, "yMin": y_min, "yMax": y_max}
        downsample_raster = el.path.raster.timestamp.getDownsampledRaster(
            pathId=dataset_ids.path_id, timestampId=dataset_ids.time_stamp_id, extent=extent,
            width=EllipsisHelper.DOWNSAMPLE_WIDTH, height=EllipsisHelper.DOWNSAMPLE_HEIGHT, epsg=EllipsisHelper.DOWNSAMPLE_EPSG
        )
        raster = downsample_raster[EllipsisHelper.DOWNSAMPLE_RASTER_KEY][:,:,0]

        # Now we use scipy to interpolate a nice line out of this
        # Scipy interpolate wishes to receive 3 arrays. One 1D array with x-coordinates, one 1D array with y-coordinates,
        # and one 2D array with values (the altitudes in this case) for the x,y coordinate grid
        # If we give this to the scipy interpolation it will return us a function that interpolates based on the given values
        # First we construct the coordinate grid
        raster_len = raster.shape[0]
        x = [ x_min + i * (x_max - x_min) / (raster_len - 1) for i in range(raster_len) ]
        y = [ y_min + i * (y_max - y_min) / (raster_len - 1) for i in range(raster_len) ]

        # Now we can create an interpolation function using scipy
        interopolation_function = interpolate.interp2d(x, y, raster, kind=EllipsisHelper.INTERPOLATION_KIND)
        # Now all that is left is to run this function on our line segment x and y coordinates an retrieve a new grid
        interpolated_raster = interopolation_function(x_points, y_points)
        # The diagonal of this grid gives us the needed line
        z_points = [interpolated_raster[x, x] for x in range(len(x_points))]

        return z_points


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