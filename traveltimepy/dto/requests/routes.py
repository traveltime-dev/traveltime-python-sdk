from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltimepy.dto import SearchId, Location, LocationId
from traveltimepy.dto.requests import Property, FullRange
from traveltimepy.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain


class ArrivalSearch(BaseModel):
    id: SearchId
    departure_location_ids: List[LocationId]
    arrival_location_id: LocationId
    arrival_time: datetime
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class DepartureSearch(BaseModel):
    id: SearchId
    arrival_location_ids: List[LocationId]
    departure_location_id: LocationId
    departure_time: datetime
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class RoutesRequest(BaseModel):
    locations: List[Location]
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]
