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
    Location,
    Property,
    PropertyProto,
    FullRange,
    Range,
    Rectangle,
    LevelOfDetail,
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
    "Location",
    "Property",
    "PropertyProto",
    "FullRange",
    "Range",
    "Rectangle",
    "LevelOfDetail",
    "TravelTimeSdk",
    "Transportation",
    "ZonesProperty",
]
