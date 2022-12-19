from datetime import datetime, time
from pydantic import BaseModel
from typing import NewType, List, Union, Optional
from typing_extensions import Literal

from traveltimepy.dto import Coordinates

PartId = NewType('PartId', str)


class BasicPart(BaseModel):
    id: PartId
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: Literal['basic']


class RoadPart(BaseModel):
    id: PartId
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: Literal['road']
    road: Optional[str]
    turn: Optional[str]


class StartEndPart(BaseModel):
    id: PartId
    mode: str
    directions: str
    distance: int
    travel_time: int
    coords: List[Coordinates]
    type: Literal['start_end']
    direction: str


class PublicTransportPart(BaseModel):
    id: PartId
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
    type: Literal['public_transport']


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
