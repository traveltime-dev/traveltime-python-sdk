from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltimepy.dto.common import Location, FullRange, Property
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_filter import TimeFilterResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.dto.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain


class ArrivalSearch(BaseModel):
    id: str
    departure_location_ids: List[str]
    arrival_location_id: str
    arrival_time: datetime
    travel_time: int
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class DepartureSearch(BaseModel):
    id: str
    arrival_location_ids: List[str]
    departure_location_id: str
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
        return TimeFilterResponse(results=flatten([response.results for response in responses]))
