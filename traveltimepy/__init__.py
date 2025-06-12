"""Python sdk for working with traveltime api"""

from importlib.metadata import version, PackageNotFoundError

from traveltimepy.async_client import AsyncClient
from traveltimepy.dto.requests.distance_map import (
    DistanceMapDepartureSearch,
    DistanceMapArrivalSearch,
)

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

from traveltimepy.dto.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
    MaxChanges,
    TransportationFast,
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
    ProtoProperty,
    FullRange,
    Range,
    Rectangle,
    DrivingTrafficModel,
)
from traveltimepy.dto.level_of_detail import LevelOfDetail, SimpleLevelOfDetail, Level

from traveltimepy.dto.requests.postcodes_zones import ZonesProperty

__all__ = [
    "__version__",
    "TransportationFast",
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
    "ProtoProperty",
    "FullRange",
    "Range",
    "Rectangle",
    "ZonesProperty",
    "DrivingTrafficModel",
    "AsyncClient",
    "DistanceMapDepartureSearch",
    "DistanceMapArrivalSearch",
    "LevelOfDetail",
    "SimpleLevelOfDetail",
    "Level",
]
