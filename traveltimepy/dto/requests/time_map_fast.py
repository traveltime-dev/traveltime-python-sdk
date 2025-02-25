from typing import List, Optional

from pydantic import BaseModel

from traveltimepy.dto.common import (
    Coordinates,
    LevelOfDetail,
    PolygonsFilter,
    RenderMode,
    Snapping,
)
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.dto.requests.time_filter_fast import Transportation


class Search(BaseModel):
    id: str
    coords: Coordinates
    transportation: Transportation
    travel_time: int
    arrival_time_period: str
    level_of_detail: Optional[LevelOfDetail]
    snapping: Optional[Snapping]
    polygons_filter: Optional[PolygonsFilter]
    render_mode: Optional[RenderMode]


class ArrivalSearches(BaseModel):
    many_to_one: List[Search]
    one_to_many: List[Search]


class TimeMapFastRequest(TravelTimeRequest[TimeMapResponse]):
    arrival_searches: ArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapFastRequest(
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

    def merge(self, responses: List[TimeMapResponse]) -> TimeMapResponse:
        return TimeMapResponse(
            results=flatten([response.results for response in responses])
        )
