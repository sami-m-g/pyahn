"""pyahn model module."""
from dataclasses import dataclass


@dataclass
class DatasetIds:
    """Datasets API parameters."""
    path_id: str
    time_stamp_id: str
