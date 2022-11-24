from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from traveltime.dto import SearchId, Location, LocationId, FullRange, Property
from traveltime.transportation import Transportation


@dataclass(frozen=True)
class ArrivalSearch:
    id: SearchId
    departure_location_ids: List[LocationId]
    arrival_location_id: LocationId
    arrival_time: datetime
    travel_time: int
    transportation: Transportation
    properties: List[Property]
    full_range: Optional[FullRange]


@dataclass(frozen=True)
class DepartureSearch:
    id: SearchId
    arrival_location_ids: List[LocationId]
    departure_location_id: LocationId
    departure_time: datetime
    travel_time: int
    transportation: Transportation
    properties: List[Property]
    full_range: Optional[FullRange]


@dataclass(frozen=True)
class TimeFilterRequest:
    locations: List[Location]
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]
