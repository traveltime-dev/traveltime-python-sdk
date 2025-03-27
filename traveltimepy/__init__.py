"""Python sdk for working with traveltime api"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    pass

from traveltimepy.dto.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
    MaxChanges,
)
from traveltimepy.dto.requests.time_filter_proto import (
    ProtoTransportation,
    ProtoCountry,
)
from traveltimepy.dto.common import (
    Coordinates,
    H3Centroid,
    GeohashCentroid,
    Location,
    Property,
    CellProperty,
    Snapping,
    PropertyProto,
    FullRange,
    Range,
    Rectangle,
    LevelOfDetail,
    DrivingTrafficModel,
)

from traveltimepy.sdk import TravelTimeSdk
from traveltimepy.dto.requests.time_filter_fast import Transportation
from traveltimepy.dto.requests.postcodes_zones import ZonesProperty

__all__ = [
    "__version__",
    "PublicTransport",
    "Driving",
    "Ferry",
    "Walking",
    "Cycling",
    "DrivingTrain",
    "CyclingPublicTransport",
    "MaxChanges",
    "ProtoTransportation",
    "ProtoCountry",
    "Coordinates",
    "H3Centroid",
    "GeohashCentroid",
    "Snapping",
    "Location",
    "Property",
    "CellProperty",
    "PropertyProto",
    "FullRange",
    "Range",
    "Rectangle",
    "LevelOfDetail",
    "TravelTimeSdk",
    "Transportation",
    "ZonesProperty",
    "DrivingTrafficModel",
]
