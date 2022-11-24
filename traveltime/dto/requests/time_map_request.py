from dataclasses import dataclass
from datetime import datetime

from typing import List, Optional

from traveltime.dto import Coordinates, SearchId, Range
from traveltime.transportation import Transportation


@dataclass(frozen=True)
class DepartureSearch:
    id: SearchId
    coords: Coordinates
    departure_time: datetime
    travel_time: int
    transportation: Transportation
    range: Optional[Range] = None


@dataclass(frozen=True)
class ArrivalSearch:
    id: SearchId
    coords: Coordinates
    arrival_time: datetime
    travel_time: int
    transportation: Transportation
    range: Optional[Range] = None


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
