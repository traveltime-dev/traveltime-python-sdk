from dataclasses import dataclass
from enum import Enum

from typing import NewType, List

SearchId = NewType('SearchId', str)
LocationId = NewType('LocationId', str)


@dataclass(frozen=True)
class Coordinates:
    lat: float
    lng: float


@dataclass(frozen=True)
class Ticket:
    type: str
    price: float
    currency: str


@dataclass(frozen=True)
class FareBreakdown:
    modes: List[str]
    route_part_ids: List[int]
    tickets: List[Ticket]


@dataclass(frozen=True)
class Fares:
    breakdown: List[FareBreakdown]
    tickets_total: List[Ticket]


@dataclass(frozen=True)
class Location:
    id: str
    coords: Coordinates


@dataclass(frozen=True)
class FullRange:
    enabled: bool
    max_results: int
    width: int


@dataclass(frozen=True)
class Range:
    enabled: bool
    width: int


class Property(str, Enum):
    TRAVEL_TIME = 'travel_time'
    DISTANCE = 'distance'
    ROUTE = 'route'
    FARES = 'fares'

