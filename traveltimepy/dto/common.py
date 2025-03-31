from datetime import datetime, time
from enum import Enum
from typing import List, Union, Optional

from pydantic import field_validator
from typing_extensions import Literal
from pydantic.main import BaseModel


class Coordinates(BaseModel):
    lat: float
    lng: float

    @field_validator("lat")
    @classmethod
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return v

    @field_validator("lng")
    @classmethod
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return v


class GeohashCentroid(BaseModel):
    geohash_centroid: str


class H3Centroid(BaseModel):
    h3_centroid: str


class Location(BaseModel):
    id: str
    coords: Coordinates

    def __hash__(self):
        return hash(self.id)


class BasicPart(BaseModel):
    id: int
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: Literal["basic"]


class RoadPart(BaseModel):
    id: int
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: Literal["road"]
    road: Optional[str] = None
    turn: Optional[str] = None


class StartEndPart(BaseModel):
    id: int
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: Literal["start_end"]
    direction: str


class PublicTransportPart(BaseModel):
    id: int
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    line: str
    departure_station: str
    arrival_station: str
    departs_at: time
    arrives_at: time
    num_stops: int
    type: Literal["public_transport"]


class Route(BaseModel):
    departure_time: datetime
    arrival_time: datetime
    parts: List[Union[BasicPart, PublicTransportPart, StartEndPart, RoadPart]]


class Ticket(BaseModel):
    type: str
    price: float
    currency: str


class FareBreakdown(BaseModel):
    modes: List[str]
    route_part_ids: List[int]
    tickets: List[Ticket]


class Fares(BaseModel):
    breakdown: List[FareBreakdown]
    tickets_total: List[Ticket]


class Rectangle(BaseModel):
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float

    def to_str(self):
        return f"{self.min_lat},{self.min_lng},{self.max_lat},{self.max_lng}"


class Property(str, Enum):
    TRAVEL_TIME = "travel_time"
    DISTANCE = "distance"
    ROUTE = "route"
    FARES = "fares"


class CellProperty(str, Enum):
    MIN = "min"
    MAX = "max"
    MEAN = "mean"


class SnappingPenalty(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class SnappingAcceptRoads(str, Enum):
    BOTH_DRIVABLE_AND_WALKABLE = "both_drivable_and_walkable"
    ANY_DRIVABLE = "any_drivable"


class DrivingTrafficModel(str, Enum):
    OPTIMISTIC = "optimistic"
    BALANCED = "balanced"
    PESSIMISTIC = "pessimistic"


class Snapping(BaseModel):
    penalty: Optional[SnappingPenalty] = SnappingPenalty.ENABLED
    accept_roads: Optional[SnappingAcceptRoads] = (
        SnappingAcceptRoads.BOTH_DRIVABLE_AND_WALKABLE
    )


class PropertyProto(int, Enum):
    DISTANCE = 1


class FullRange(BaseModel):
    enabled: bool
    max_results: int
    width: int


class Range(BaseModel):
    enabled: bool
    width: int


class LevelOfDetail(BaseModel):
    scale_type: Literal["simple", "simple_numeric", "coarse_grid"] = "simple"
    level: Optional[Union[int, str]] = None
    square_size: Optional[int] = None


class PolygonsFilter(BaseModel):
    limit: int


class RenderMode(str, Enum):
    APPROXIMATE_TIME_FILTER = "approximate_time_filter"
    ROAD_BUFFERING = "road_buffering"


class TimeInfo:
    def __init__(self, time_value: datetime):
        self.value = time_value


class DepartureTime(TimeInfo):
    pass


class ArrivalTime(TimeInfo):
    pass
