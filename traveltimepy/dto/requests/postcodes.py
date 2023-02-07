from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel

from traveltimepy.dto.common import Coordinates, Property, FullRange
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.postcodes import PostcodesResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.dto.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain


class ArrivalSearch(BaseModel):
    id: str
    coords: Coordinates
    travel_time: int
    arrival_time: datetime
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class DepartureSearch(BaseModel):
    id: str
    coords: Coordinates
    travel_time: int
    departure_time: datetime
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    full_range: Optional[FullRange] = None


class PostcodesRequest(TravelTimeRequest[PostcodesResponse]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self) -> List[TravelTimeRequest]:
        return [
            PostcodesRequest(departure_searches=departures, arrival_searches=arrivals)
            for departures, arrivals in split(self.departure_searches, self.arrival_searches, 10)
        ]

    def merge(self, responses: List[PostcodesResponse]) -> PostcodesResponse:
        return PostcodesResponse(
            results=sorted(flatten([response.results for response in responses]), key=lambda res: res.search_id)
        )
