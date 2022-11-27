from enum import Enum

from typing import NewType, List

from pydantic.main import BaseModel

SearchId = NewType('SearchId', str)
LocationId = NewType('LocationId', str)


class Coordinates(BaseModel):
    lat: float
    lng: float


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


class Location(BaseModel):
    id: str
    coords: Coordinates


class FullRange(BaseModel):
    enabled: bool
    max_results: int
    width: int


class Range(BaseModel):
    enabled: bool
    width: int


class Property(str, Enum):
    TRAVEL_TIME = 'travel_time'
    DISTANCE = 'distance'
    ROUTE = 'route'
    FARES = 'fares'

