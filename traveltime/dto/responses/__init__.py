from datetime import datetime, time
from pydantic import BaseModel
from typing import Literal, NewType, List, Union, Optional

from traveltime.dto import Coordinates

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
