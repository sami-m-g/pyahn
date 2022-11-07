from dataclasses import dataclass
from typing import ClassVar


@dataclass
class UrlParams:
    image_sr_key: ClassVar[str] = "&imageSR="
    time_key: ClassVar[str] = "&time="
    format_key: ClassVar[str] = "&format="
    pixel_type_key : ClassVar[str] = "&pixelType="
    no_data_interpolation_key : ClassVar[str] = "&noDataInterpretation="
    interpolation_key : ClassVar[str] = "&interpolation="
    compression_key: ClassVar[str]  ="&compression="
    compression_quality_key : ClassVar[str] = "&compressionQuality="
    bands_ids_key: ClassVar[str] = "&bandIds="
    mosaic_rule_key: ClassVar[str] = "&mosaicRule="
    rendering_rule_key: ClassVar[str] = "&renderingRule="
    f_key : ClassVar[str] = "&f="

    image_sr: str  = ""
    time: str = ""
    format: str = "tiff"
    pixel_type: str = "F64"
    no_data_interpolation: str = "esriNoDataMatchAny"
    interpolation: str  = "+RSP_BilinearInterpolation"
    compression: str = ""
    compression_quality: int  = 100
    bands_ids: str = ""
    mosaic_rule: str  = ""
    rendering_rule: str = ""
    f: str = "image"

    def to_string(self) -> str:
        return f"{self.image_sr_key}{self.image_sr}"                        \
            f"{self.time_key}{self.time}"                                   \
            f"{self.format_key}{self.format}"                               \
            f"{self.pixel_type_key}{self.pixel_type}"                       \
            f"{self.no_data_interpolation_key}{self.no_data_interpolation}" \
            f"{self.interpolation_key}{self.interpolation}"                 \
            f"{self.compression_key}{self.compression}"                     \
            f"{self.compression_quality_key}{self.compression_quality}"     \
            f"{self.bands_ids_key}{self.bands_ids}"                         \
            f"{self.mosaic_rule_key}{self.mosaic_rule}"                     \
            f"{self.rendering_rule_key}{self.rendering_rule}"               \
            f"{self.f_key}{self.f}"