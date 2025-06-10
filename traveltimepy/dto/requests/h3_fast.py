from typing import List, Optional
import typing

from pydantic import BaseModel, field_serializer

from traveltimepy.dto.common import (
    CellProperty,
    Coordinates,
    H3Centroid,
    Snapping,
    ArrivalTimePeriod,
)
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.h3 import H3Response
from traveltimepy.itertools import split, flatten
from traveltimepy import TransportationFast


class H3FastSearch(BaseModel):
    id: str
    coords: typing.Union[Coordinates, H3Centroid]
    transportation: TransportationFast
    travel_time: int
    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    snapping: Optional[Snapping] = None

    # JSON expects `"transportation": { "type": "public_transport" }` and not `"transportation": "public_transport"`
    @field_serializer("transportation")
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class H3FastArrivalSearches(BaseModel):
    many_to_one: List[H3FastSearch]
    one_to_many: List[H3FastSearch]


class H3FastRequest(TravelTimeRequest[H3Response]):
    resolution: int
    properties: List[CellProperty]
    arrival_searches: H3FastArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            H3FastRequest(
                resolution=self.resolution,
                properties=self.properties,
                arrival_searches=H3FastArrivalSearches(
                    one_to_many=one_to_many, many_to_one=many_to_one
                ),
            )
            for one_to_many, many_to_one in split(
                self.arrival_searches.one_to_many,
                self.arrival_searches.many_to_one,
                window_size,
            )
        ]

    def merge(self, responses: List[H3Response]) -> H3Response:
        return H3Response(results=flatten([response.results for response in responses]))
