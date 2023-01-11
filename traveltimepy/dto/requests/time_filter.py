from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltimepy.dto import SearchId, Location, LocationId
from traveltimepy.dto.requests import FullRange, Property, flatten
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_filter import TimeFilterResponse
from traveltimepy.itertools import split
from traveltimepy.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain


class ArrivalSearch(BaseModel):
    id: SearchId
    departure_location_ids: List[LocationId]
    arrival_location_id: LocationId
    arrival_time: datetime
    travel_time: int
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class DepartureSearch(BaseModel):
    id: SearchId
    arrival_location_ids: List[LocationId]
    departure_location_id: LocationId
    departure_time: datetime
    travel_time: int
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class TimeFilterRequest(TravelTimeRequest[TimeFilterResponse]):
    locations: List[Location]
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self) -> List[TravelTimeRequest]:
        return [
            TimeFilterRequest(locations=self.locations, departure_searches=departures, arrival_searches=arrivals)
            for departures, arrivals in split(self.departure_searches, self.arrival_searches, 10)
        ]

    def merge(self, responses: List[TimeFilterResponse]) -> TimeFilterResponse:
        return TimeFilterResponse(results=list(flatten([response.results for response in responses])))
