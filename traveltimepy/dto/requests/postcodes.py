from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel

from traveltimepy.dto import SearchId, Coordinates
from traveltimepy.dto.requests import Property, FullRange
from traveltimepy.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain


class ArrivalSearch(BaseModel):
    id: SearchId
    coords: Coordinates
    travel_time: int
    arrival_time: datetime
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class DepartureSearch(BaseModel):
    id: SearchId
    coords: Coordinates
    travel_time: int
    departure_time: datetime
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class PostcodesRequest(BaseModel):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]
