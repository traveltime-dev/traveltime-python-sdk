from dataclasses import dataclass
from datetime import datetime

from typing import List

from traveltime import Coordinate, SearchId
from traveltime.transportation import Transportation


@dataclass(frozen=True)
class DepartureSearch:
    id: SearchId
    coord: Coordinate
    departure_time: datetime
    travel_time: int
    transportation: Transportation


@dataclass(frozen=True)
class ArrivalSearch:
    id: SearchId
    coord: Coordinate
    arrival_time: datetime
    travel_time: int
    transportation: Transportation


@dataclass(frozen=True)
class Intersection:
    id: SearchId
    search_ids: List[SearchId]


@dataclass(frozen=True)
class Union:
    id: SearchId
    search_ids: List[SearchId]


@dataclass(frozen=True)
class TimeMapRequest:
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]
    unions: List[Union]
    intersections: List[Intersection]
