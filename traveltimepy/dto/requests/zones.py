from datetime import datetime
from enum import Enum
from typing import List, Union, Optional

from pydantic import BaseModel

from traveltimepy.dto import SearchId, Coordinates
from traveltimepy.dto.requests import FullRange
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.zones import DistrictsResponse, SectorsResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain


class ZonesProperty(str, Enum):
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
    properties: List[ZonesProperty]
    full_range: Optional[FullRange] = None


class DepartureSearch(BaseModel):
    id: SearchId
    coords: Coordinates
    travel_time: int
    departure_time: datetime
    reachable_postcodes_threshold: float
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[ZonesProperty]
    full_range: Optional[FullRange] = None


class SectorsRequest(TravelTimeRequest[SectorsResponse]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self) -> List[TravelTimeRequest]:
        return [
            SectorsRequest(departure_searches=departures, arrival_searches=arrivals)
            for departures, arrivals in split(self.departure_searches, self.arrival_searches, 10)
        ]

    def merge(self, responses: List[SectorsResponse]) -> SectorsResponse:
        return SectorsResponse(results=flatten([response.results for response in responses]))


class DistrictsRequest(TravelTimeRequest[DistrictsResponse]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self) -> List[TravelTimeRequest]:
        return [
            DistrictsRequest(departure_searches=departures, arrival_searches=arrivals)
            for departures, arrivals in split(self.departure_searches, self.arrival_searches, 10)
        ]

    def merge(self, responses: List[DistrictsResponse]) -> DistrictsResponse:
        return DistrictsResponse(results=flatten([response.results for response in responses]))
