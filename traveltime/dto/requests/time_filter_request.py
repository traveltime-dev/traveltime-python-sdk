from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltime.dto import SearchId, Location, LocationId, FullRange, Property
from traveltime.transportation import Bus, PublicTransport, Driving


class ArrivalSearch(BaseModel):
    id: SearchId
    departure_location_ids: List[LocationId]
    arrival_location_id: LocationId
    arrival_time: datetime
    travel_time: int
    transportation: Union[Bus, PublicTransport, Driving]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class DepartureSearch(BaseModel):
    id: SearchId
    arrival_location_ids: List[LocationId]
    departure_location_id: LocationId
    departure_time: datetime
    travel_time: int
    transportation: Union[Bus, PublicTransport, Driving]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class TimeFilterRequest(BaseModel):
    locations: List[Location]
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]
