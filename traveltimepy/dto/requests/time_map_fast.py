from typing import List, Optional

from pydantic import BaseModel, field_serializer

from traveltimepy.dto.common import (
    Coordinates,
    PolygonsFilter,
    RenderMode,
    Snapping,
    ArrivalTimePeriod,
)
from traveltimepy import LevelOfDetail
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.dto.requests.time_filter_fast import TransportationFast


class TimeMapFastSearch(BaseModel):
    id: str
    coords: Coordinates
    transportation: TransportationFast
    travel_time: int
    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    level_of_detail: Optional[LevelOfDetail] = None
    snapping: Optional[Snapping] = None
    polygons_filter: Optional[PolygonsFilter] = None
    render_mode: Optional[RenderMode] = None

    # JSON expects `"transportation": { "type": "public_transport" }` and not `"transportation": "public_transport"`
    @field_serializer("transportation")
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class TimeMapFastArrivalSearches(BaseModel):
    many_to_one: List[TimeMapFastSearch]
    one_to_many: List[TimeMapFastSearch]


class TimeMapFastRequest(TravelTimeRequest[TimeMapResponse]):
    arrival_searches: TimeMapFastArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapFastRequest(
                arrival_searches=TimeMapFastArrivalSearches(
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
