from typing import List

from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.requests.time_map import (
    DepartureSearch,
    ArrivalSearch,
)
from traveltimepy.dto.responses.time_map_kml import TimeMapKmlResponse
from traveltimepy.itertools import split, flatten


class TimeMapRequestKML(TravelTimeRequest[TimeMapKmlResponse]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapRequestKML(
                departure_searches=departures,
                arrival_searches=arrivals,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[TimeMapKmlResponse]) -> TimeMapKmlResponse:
        merged_features = flatten([response.results for response in responses])
        return TimeMapKmlResponse(results=merged_features)
