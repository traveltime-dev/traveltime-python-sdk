from typing import List
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.requests.time_map_fast import ArrivalSearches
from traveltimepy.dto.responses.time_map_wkt import TimeMapWKTResponse
from traveltimepy.itertools import split, flatten


class TimeMapFastWKTRequest(TravelTimeRequest[TimeMapWKTResponse]):
    arrival_searches: ArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapFastWKTRequest(
                arrival_searches=ArrivalSearches(
                    one_to_many=one_to_many, many_to_one=many_to_one
                ),
            )
            for one_to_many, many_to_one in split(
                self.arrival_searches.one_to_many,
                self.arrival_searches.many_to_one,
                window_size,
            )
        ]

    def merge(self, responses: List[TimeMapWKTResponse]) -> TimeMapWKTResponse:
        return TimeMapWKTResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
