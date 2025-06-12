from datetime import datetime, time
from enum import Enum
from typing import List, Union, Optional

from pydantic import field_validator, Field
from typing_extensions import Literal
from pydantic.main import BaseModel


class Coordinates(BaseModel):
    """
    Represents geographical coordinates with latitude and longitude.

    Attributes:
        lat: Latitude coordinate (-90.0 to 90.0)
        lng: Longitude coordinate (-180.0 to 180.0)
    """

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
    """
    Represents a rectangular geographic bounding box defined by minimum and maximum latitude and longitude coordinates.
    """

    min_lat: float
    """
    The minimum latitude (southern boundary) of the rectangle in decimal degrees.
    Valid range: -90.0 to +90.0, where negative values represent the Southern Hemisphere.
    """

    max_lat: float
    """
    The maximum latitude (northern boundary) of the rectangle in decimal degrees.
    Valid range: -90.0 to +90.0, where positive values represent the Northern Hemisphere.
    """

    min_lng: float
    """
    The minimum longitude (western boundary) of the rectangle in decimal degrees.
    Valid range: -180.0 to +180.0, where negative values represent the Western Hemisphere.
    """

    max_lng: float
    """
    The maximum longitude (eastern boundary) of the rectangle in decimal degrees.
    Valid range: -180.0 to +180.0, where positive values represent the Eastern Hemisphere.
    """

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
    """
    Determines how off-road distances are factored into journey calculations.
    Controls whether the time/distance required to reach the actual road network is included in metrics.
    """

    ENABLED = "enabled"
    """
    Walking time and distance from the departure location to the nearest road
    and from the nearest road to the arrival location are added to the total travel time and distance of a journey.
    This provides more realistic door-to-door journey metrics that include the "first and last mile" segments.
    """

    DISABLED = "disabled"
    """
    Walking times and distances are not added to the total reported values
    (i.e., the journey effectively starts and ends at the nearest points on the road network).
    This approach focuses exclusively on the road network portion of a journey,
    which may be preferred for vehicle-only routing or when endpoints are already on roads.
    """


class SnappingAcceptRoads(str, Enum):
    """
    Defines which road types are valid for journey start/end points based on their accessibility characteristics.
    This affects where a journey can begin or terminate within the routing network.
    """

    BOTH_DRIVABLE_AND_WALKABLE = "both_drivable_and_walkable"
    """
    Journey can only start or end on roads that are accessible by both cars and pedestrians.
    This effectively means journeys cannot start/end on motorways, highways, or other vehicle-only roadways.
    Ensures journey endpoints are accessible to pedestrians, which is important for first/last mile connectivity.
    """

    ANY_DRIVABLE = "any_drivable"
    """
    Journey can start or end on any road accessible by a car (including motorways).
    This option maximizes vehicle routing options by allowing connections to all drivable roads,
    but may result in journey endpoints that are not accessible to pedestrians.
    """


class DrivingTrafficModel(str, Enum):
    OPTIMISTIC = "optimistic"
    BALANCED = "balanced"
    PESSIMISTIC = "pessimistic"


class ArrivalTimePeriod(str, Enum):
    WEEKDAY_MORNING = "weekday_morning"


class Snapping(BaseModel):
    """
    Configuration for how journey calculations handle connections between arbitrary points and the road network.

    "Snapping" refers to the process of connecting departure/arrival locations to the nearest suitable roads
    "Snapping" refers to the process of connecting departure/arrival locations to the nearest suitable roads
    and determining how the off-road portions of journeys are calculated and reported.
    """

    penalty: Optional[SnappingPenalty] = SnappingPenalty.ENABLED
    """
    Controls whether off-road walking distances are included in total journey metrics.
    When enabled, includes "first and last mile" walking times/distances for more realistic door-to-door calculations.
    """

    accept_roads: Optional[SnappingAcceptRoads] = (
        SnappingAcceptRoads.BOTH_DRIVABLE_AND_WALKABLE
    )
    """
    Defines which road types are valid as journey start/end points.
    Determines whether journeys can snap to vehicle-only roads (like motorways) or only pedestrian-accessible roads.
    """


class ProtoProperty(int, Enum):
    DISTANCE = 1


class FullRange(BaseModel):
    enabled: bool
    max_results: int
    width: int


class Range(BaseModel):
    enabled: bool
    width: int


class PolygonsFilter(BaseModel):
    """
    Specifies polygon filter configuration for limiting the number of polygons returned.

    Attributes:
        limit: Maximum number of largest polygons to return in a single shape.
               Must be greater than 0.
    """

    limit: int = Field(gt=0)


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
