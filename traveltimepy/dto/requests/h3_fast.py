from typing import List, Optional
import typing

from pydantic import BaseModel

from traveltimepy.dto.common import (
    CellProperty,
    Coordinates,
    H3Centroid,
    Snapping,
)
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.h3 import H3Response
from traveltimepy.itertools import split, flatten
from traveltimepy.dto.requests.time_filter_fast import Transportation


class Search(BaseModel):
    id: str
    coords: typing.Union[Coordinates, H3Centroid]
    transportation: Transportation
    travel_time: int
    arrival_time_period: str
    snapping: Optional[Snapping]


class ArrivalSearches(BaseModel):
    many_to_one: List[Search]
    one_to_many: List[Search]


class H3FastRequest(TravelTimeRequest[H3Response]):
    resolution: int
    properties: List[CellProperty]
    arrival_searches: ArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            H3FastRequest(
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

    def merge(self, responses: List[H3Response]) -> H3Response:
        return H3Response(results=flatten([response.results for response in responses]))
