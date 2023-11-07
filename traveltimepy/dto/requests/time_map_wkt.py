from typing import List
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.requests.time_map import DepartureSearch, ArrivalSearch
from traveltimepy.dto.responses.time_map_wkt import TimeMapWKTResponse
from traveltimepy.itertools import split, flatten


class TimeMapWKTRequest(TravelTimeRequest[TimeMapWKTResponse]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapWKTRequest(departure_searches=departures, arrival_searches=arrivals)
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
