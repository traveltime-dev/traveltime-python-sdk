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
    """
    Represents a geographic location using a geohash centroid string.

    Attributes:
        geohash_centroid: Geohash string representing the centroid of a geographic cell.
                         Used as an alternative to lat/lng coordinates for specifying
                         departure or arrival locations.
    """

    geohash_centroid: str


class H3Centroid(BaseModel):
    """Geographic location using H3 hexagonal cell centroid.

    Attributes:
        h3_centroid (str): H3 index string identifying a hexagonal cell.
            Typically, a 15-character hexadecimal value.
    """

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

    Attributes:
        min_lat: The minimum latitude (southern boundary) of the rectangle in decimal degrees.
                Valid range: -90.0 to +90.0, where negative values represent the Southern Hemisphere.
        max_lat: The maximum latitude (northern boundary) of the rectangle in decimal degrees.
                Valid range: -90.0 to +90.0, where positive values represent the Northern Hemisphere.
        min_lng: The minimum longitude (western boundary) of the rectangle in decimal degrees.
                Valid range: -180.0 to +180.0, where negative values represent the Western Hemisphere.
        max_lng: The maximum longitude (eastern boundary) of the rectangle in decimal degrees.
                Valid range: -180.0 to +180.0, where positive values represent the Eastern Hemisphere.
    """

    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float

    def to_str(self):
        return f"{self.min_lat},{self.min_lng},{self.max_lat},{self.max_lng}"


class Property(str, Enum):
    """
    Defines what data should be returned in API responses. Different endpoints
    support different combinations of these properties.

    Attributes:
        TRAVEL_TIME: Journey time in seconds
        DISTANCE: Journey distance in meters
        ROUTE: Detailed route information with turn-by-turn directions
        FARES: Public transport fare information (where available)
    """

    TRAVEL_TIME = "travel_time"
    DISTANCE = "distance"
    ROUTE = "route"
    FARES = "fares"


class CellProperty(str, Enum):
    """
    Travel time properties that can be calculated and returned for each cell.

    Attributes:
        MIN: Minimum travel time to any point of interest within cell.
        MAX: Maximum travel time to any point of interest within cell.
        MEAN: Mean travel time to points of interest within cell.
    """

    MIN = "min"
    MAX = "max"
    MEAN = "mean"


class SnappingPenalty(str, Enum):
    """
    Determines how off-road distances are factored into journey calculations.
    Controls whether the time/distance required to reach the actual road network is included in metrics.

    Attributes:
        ENABLED: Walking time and distance from departure to nearest road and from nearest road
                to arrival are added to total travel time and distance. Provides realistic door-to-door metrics.
        DISABLED: Walking times and distances are not added to reported values. Journey effectively
                 starts and ends at nearest points on the road network.
    """

    ENABLED = "enabled"
    DISABLED = "disabled"


class SnappingAcceptRoads(str, Enum):
    """
    Defines which road types are valid for journey start/end points based on their accessibility characteristics.
    This affects where a journey can begin or terminate within the routing network.

    Attributes:
        BOTH_DRIVABLE_AND_WALKABLE: Journey can only start or end on roads accessible by both cars and pedestrians.
                                   Effectively means journeys cannot start/end on motorways or vehicle-only roads.
        ANY_DRIVABLE: Journey can start or end on any road accessible by a car (including motorways).
                     Maximizes vehicle routing options but may result in pedestrian-inaccessible endpoints.
    """

    BOTH_DRIVABLE_AND_WALKABLE = "both_drivable_and_walkable"
    ANY_DRIVABLE = "any_drivable"


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
    and determining how the off-road portions of journeys are calculated and reported.

    Attributes:
        penalty: Controls whether off-road walking distances are included in total journey metrics.
                When enabled, includes "first and last mile" walking times/distances for realistic door-to-door calculations.
        accept_roads: Defines which road types are valid as journey start/end points.
                     Determines whether journeys can snap to vehicle-only roads or only pedestrian-accessible roads.
    """

    penalty: Optional[SnappingPenalty] = SnappingPenalty.ENABLED
    accept_roads: Optional[SnappingAcceptRoads] = (
        SnappingAcceptRoads.BOTH_DRIVABLE_AND_WALKABLE
    )


class ProtoProperty(int, Enum):
    DISTANCE = 1


class FullRange(BaseModel):
    """
    Configures time range search parameters for journey planning.

    When enabled, allows searches to consider journeys within a specified
    time window rather than at an exact time only, providing multiple journey options.
    """

    enabled: bool
    """
    Controls whether the time range search is active.

    When enabled, adds a time window to the specified departure or arrival time.
    Journey results will include any options that depart/arrive within this window.

    Note:
    - Disabled by default
    - Only supported for public transportation modes (public_transport, coach, bus,
      train, driving+train, driving+public_transport, cycling+public_transport)
    - Ignored for other transportation modes
    """

    max_results: int = Field(gt=0, le=5)
    """
    Maximum number of results to return. Limited to 5 results.
    Must be greater than 0.
    """

    width: int = Field(gt=0, le=43200)
    """
    Defines the width of the time range window in seconds.

    Behavior varies based on whether searching by departure or arrival time:
    - For departure time: Window extends forward (e.g., 9:00am with 1-hour width
      includes journeys departing 9:00am-10:00am)
    - For arrival time: Window extends backward (e.g., 9:00am with 1-hour width
      includes journeys arriving 8:00am-9:00am)

    Must be greater than 0. Maximum allowed value: 43,200 seconds (12 hours).
    """


class Range(BaseModel):
    """
    Configures time range parameters for route searching.

    When enabled, allows searching for routes departing or arriving within a time window
    rather than at a single specific time, returning a combined result that represents
    all possible journeys within that window.

    Time range functionality is primarily applicable to scheduled transportation modes:
    public_transport, coach, bus, train, and driving+train combinations.
    For other transportation modes (walking, cycling, driving), these parameters are ignored.
    """

    enabled: bool
    """
    Controls whether the time range functionality is active.

    When True, the routing algorithm considers departures or arrivals within a window:
    - For departure searches: starting between the specified departure time and
      'width' seconds in the future from that departure time
    - For arrival searches: finishing between the specified arrival time and
      'width' seconds in the past from that arrival time

    When False, only the exact departure or arrival time is considered,
    and the width parameter is ignored.
    """

    width: int
    """
    Duration of the time window in seconds.

    For departure searches: Window starts at departure time and extends forward.
    Example: departure time 09:00 with width 3600 (1 hour) includes all journeys
    departing between 09:00 and 10:00.

    For arrival searches: Window ends at arrival time and extends backward.
    Example: arrival time 17:00 with width 3600 (1 hour) includes all journeys
    arriving between 16:00 and 17:00.

    Must be positive. Maximum allowed value is 43200 (12 hours).
    """


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
