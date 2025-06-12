from typing import List
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.requests.time_map import (
    TimeMapDepartureSearch,
    TimeMapArrivalSearch,
)
from traveltimepy.responses.time_map_wkt import TimeMapWKTResponse
from traveltimepy.itertools import split, flatten


class TimeMapWktRequest(TravelTimeRequest[TimeMapWKTResponse]):
    departure_searches: List[TimeMapDepartureSearch]
    arrival_searches: List[TimeMapArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapWktRequest(departure_searches=departures, arrival_searches=arrivals)
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[TimeMapWKTResponse]) -> TimeMapWKTResponse:
        return TimeMapWKTResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
