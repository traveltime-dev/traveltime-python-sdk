import abc
from datetime import datetime, time
from enum import Enum
from typing import List, Optional, Union

from pydantic.main import BaseModel
from typing_extensions import Literal


class Coordinates(BaseModel):
    lat: float
    lng: float

    def __hash__(self):
        return hash((self.lat, self.lng))


class Location(BaseModel):
    id: str
    coords: Coordinates

    def __hash__(self):
        return hash(self.id)


class BasePart(BaseModel, abc.ABC):
    id: str
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: str

    def __hash__(self):
        return hash((self.mode, self.directions, self.distance, self.travel_time, self.coords, self.type))

    def __eq__(self, other):
        """
        Equality comparison excludes id field which is
         an information about the instance relationship with other part instances
         and not an information about the part itself (i.e. otherwise identical parts could
         have different IDs in different routes).
        """
        if not isinstance(other, BasePart):
            return NotImplemented
        return (self.mode, self.directions, self.distance, self.travel_time, self.coords, self.type) == (
            other.mode,
            other.directions,
            other.distance,
            other.travel_time,
            other.coords,
            other.type,
        )


class BasicPart(BasePart):
    type: Literal["basic"]


class RoadPart(BasePart):
    type: Literal["road"]
    road: Optional[str]
    turn: Optional[str]

    def __hash__(self):
        return hash(
            (
                super().__hash__(),
                self.road,
                self.turn,
            )
        )

    def __eq__(self, other):
        if not isinstance(other, RoadPart):
            return NotImplemented
        return super().__eq__(other) and (self.road, self.turn) == (other.road, other.turn)


class StartEndPart(BasePart):
    type: Literal["start_end"]
    direction: str

    def __hash__(self):
        return hash((super().__hash__(), self.direction))

    def __eq__(self, other):
        if not isinstance(other, StartEndPart):
            return NotImplemented
        return super().__eq__(other) and self.direction == other.direction


class PublicTransportPart(BasePart):
    line: str
    departure_station: str
    arrival_station: str
    departs_at: time
    arrives_at: time
    num_stops: int
    type: Literal["public_transport"]


def __hash__(self):
    return hash(
        (
            super().__hash__(),
            self.line,
            self.departure_station,
            self.arrival_station,
            self.departs_at,
            self.arrives_at,
            self.num_stops,
        )
    )


def __eq__(self, other):
    if not isinstance(other, PublicTransportPart):
        return NotImplemented
    return super().__eq__(other) and (
        self.line,
        self.departure_station,
        self.arrival_station,
        self.departs_at,
        self.arrives_at,
        self.num_stops,
    ) == (
        other.line,
        other.departure_station,
        other.arrival_station,
        other.departs_at,
        other.arrives_at,
        other.num_stops,
    )


class Route(BaseModel):
    departure_time: datetime
    arrival_time: datetime
    parts: List[Union[BasicPart, PublicTransportPart, StartEndPart, RoadPart]]

    def __hash__(self):
        return hash((self.departure_time, self.arrival_time, *self.parts))

    def __eq__(self, other):
        if not isinstance(other, Route):
            return NotImplemented
        return (self.departure_time, self.arrival_time, self.parts) == (
            other.departure_time,
            other.arrival_time,
            other.parts,
        )


class Ticket(BaseModel):
    type: str
    price: float
    currency: str

    def __hash__(self):
        return hash((self.type, self.price, self.currency))

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return NotImplemented
        return (self.type, self.price, self.currency) == (other.type, other.price, other.currency)


class FareBreakdown(BaseModel):
    modes: List[str]
    route_part_ids: List[int]
    tickets: List[Ticket]

    def __hash__(self):
        return hash((*self.modes, *self.route_part_ids, *self.tickets))

    def __eq__(self, other):
        if not isinstance(other, FareBreakdown):
            return NotImplemented
        return (self.modes, self.route_part_ids, self.tickets) == (other.modes, other.route_part_ids, other.tickets)


class Fares(BaseModel):
    breakdown: List[FareBreakdown]
    tickets_total: List[Ticket]

    def __hash__(self):
        return hash((*self.breakdown, *self.tickets_total))

    def __eq__(self, other):
        if not isinstance(other, Fares):
            return NotImplemented
        return (self.breakdown, self.tickets_total) == (other.breakdown, other.tickets_total)


class Rectangle(BaseModel):
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float

    def to_str(self):
        return f"{self.min_lat},{self.min_lng},{self.max_lat},{self.max_lng}"

    def __hash__(self):
        return hash((self.min_lat, self.max_lat, self.min_lng, self.max_lng))

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return (self.min_lat, self.max_lat, self.min_lng, self.max_lng) == (
            other.min_lat,
            other.max_lat,
            other.min_lng,
            other.max_lng,
        )


class Property(str, Enum):
    TRAVEL_TIME = "travel_time"
    DISTANCE = "distance"
    ROUTE = "route"
    FARES = "fares"


class FullRange(BaseModel):
    enabled: bool
    max_results: int
    width: int

    def __hash__(self):
        return hash((self.enabled, self.max_results, self.width))

    def __eq__(self, other):
        if not isinstance(other, FullRange):
            return NotImplemented
        return (self.enabled, self.max_results, self.width) == (other.enabled, other.max_results, other.width)


class Range(BaseModel):
    enabled: bool
    width: int

    def __hash__(self):
        return hash((self.enabled, self.width))

    def __eq__(self, other):
        if not isinstance(other, Range):
            return NotImplemented
        return (self.enabled, self.width) == (other.enabled, other.width)
