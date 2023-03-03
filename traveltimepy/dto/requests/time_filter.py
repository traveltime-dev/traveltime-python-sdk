from datetime import datetime
from typing import List, Optional, Union

from pydantic import Field
from pydantic.main import BaseModel

from traveltimepy.dto.common import FullRange, Location, Property
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_filter import TimeFilterResponse
from traveltimepy.dto.transportation import Cycling, Driving, DrivingTrain, Ferry, PublicTransport, Walking
from traveltimepy.itertools import flatten, split


class ArrivalSearch(BaseModel):
    id: str
    departure_location_ids: List[str]
    arrival_location_id: str
    arrival_time: datetime
    travel_time: int
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    range: Optional[FullRange] = Field(None, alias="full_range")


class DepartureSearch(BaseModel):
    id: str
    arrival_location_ids: List[str]
    departure_location_id: str
    departure_time: datetime
    travel_time: int
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    range: Optional[FullRange] = Field(None, alias="full_range")


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
