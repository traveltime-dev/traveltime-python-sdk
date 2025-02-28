from typing import List, Optional
import typing

from pydantic import BaseModel

from traveltimepy.dto.common import (
    CellProperty,
    Coordinates,
    GeohashCentroid,
    Snapping,
)
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.geohash import GeohashResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.dto.requests.time_filter_fast import Transportation


class Search(BaseModel):
    id: str
    coords: typing.Union[Coordinates, GeohashCentroid]
    transportation: Transportation
    travel_time: int
    arrival_time_period: str
    snapping: Optional[Snapping]


class ArrivalSearches(BaseModel):
    many_to_one: List[Search]
    one_to_many: List[Search]


class GeohashFastRequest(TravelTimeRequest[GeohashResponse]):
    resolution: int
    properties: List[CellProperty]
    arrival_searches: ArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            GeohashFastRequest(
                resolution=self.resolution,
                properties=self.properties,
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

    def merge(self, responses: List[GeohashResponse]) -> GeohashResponse:
        return GeohashResponse(
            results=flatten([response.results for response in responses])
        )
