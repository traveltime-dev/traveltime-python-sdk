from datetime import datetime
from enum import Enum
from typing import List, Union, Optional

from pydantic import BaseModel

from traveltimepy.dto import SearchId, Coordinates
from traveltimepy.dto.requests import FullRange
from traveltimepy.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain


class Property(str, Enum):
    TRAVEL_TIME_REACHABLE = 'travel_time_reachable'
    TRAVEL_TIME_ALL = 'travel_time_all'
    COVERAGE = 'coverage'


class ArrivalSearch(BaseModel):
    id: SearchId
    coords: Coordinates
    travel_time: int
    arrival_time: datetime
    reachable_postcodes_threshold: float
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class DepartureSearch(BaseModel):
    id: SearchId
    coords: Coordinates
    travel_time: int
    departure_time: datetime
    reachable_postcodes_threshold: float
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class SectorsRequest(BaseModel):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]


class DistrictsRequest(BaseModel):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]
