import abc
from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltimepy.dto.common import FullRange, Location, Property
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_filter import TimeFilterResponse
from traveltimepy.dto.transportation import Cycling, Driving, DrivingTrain, Ferry, PublicTransport, Walking
from traveltimepy.itertools import flatten, split


class BaseTimeFilterSearch(BaseModel, abc.ABC):
    id: str
    travel_time: int
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    range: Optional[FullRange] = None

    def __hash__(self):
        return hash((self.id, self.travel_time, self.transportation, *self.properties, self.range))


class ArrivalSearch(BaseTimeFilterSearch):
    departure_location_ids: List[str]
    arrival_location_id: str
    arrival_time: datetime

    def __hash__(self):
        """Has includes class name to ensure hashes of ArrivalSearch and DepartureSearch are never equal"""

        return hash(
            (
                'ArrivalSearch',
                super().__hash__(),
                *self.departure_location_ids,
                self.arrival_location_id,
                self.arrival_time,
            )
        )


class DepartureSearch(BaseTimeFilterSearch):
    arrival_location_ids: List[str]
    departure_location_id: str
    departure_time: datetime

    def __hash__(self):
        """Has includes class name to ensure hashes of ArrivalSearch and DepartureSearch are never equal"""

        return hash(
            (
                'DepartureSearch',
                super().__hash__(),
                self.departure_location_id,
                *self.arrival_location_ids,
                self.departure_time,
            )
        )


class TimeFilterRequest(TravelTimeRequest[TimeFilterResponse]):
    locations: List[Location]
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeFilterRequest(locations=self.locations, departure_searches=departures, arrival_searches=arrivals)
            for departures, arrivals in split(self.departure_searches, self.arrival_searches, window_size)
        ]

    def merge(self, responses: List[TimeFilterResponse]) -> TimeFilterResponse:
        return TimeFilterResponse(results=flatten([response.results for response in responses]))
