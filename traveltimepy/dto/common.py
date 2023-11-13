from datetime import datetime, time
from enum import Enum
from typing import List, Union, Optional

from pydantic import validator
from typing_extensions import Literal
from pydantic.main import BaseModel


class Coordinates(BaseModel):
    lat: float
    lng: float

    @validator("lat")
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return v

    @validator("lng")
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return v


class Location(BaseModel):
    id: str
    coords: Coordinates

    def __hash__(self):
        return hash(self.id)


class BasicPart(BaseModel):
    id: str
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: Literal["basic"]


class RoadPart(BaseModel):
    id: str
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: Literal["road"]
    road: Optional[str]
    turn: Optional[str]


class StartEndPart(BaseModel):
    id: str
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: Literal["start_end"]
    direction: str


class PublicTransportPart(BaseModel):
    id: str
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
    level: Optional[Union[int, str]]
    square_size: Optional[int]
