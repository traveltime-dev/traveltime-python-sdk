from typing import List, Optional
import typing

from pydantic import BaseModel, field_serializer

from traveltimepy.dto.common import (
    CellProperty,
    Coordinates,
    GeohashCentroid,
    Snapping, ArrivalTimePeriod,
)
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.geohash import GeoHashResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.dto.requests.time_filter_fast import TransportationFast


class GeoHashFastSearch(BaseModel):
    id: str
    coords: typing.Union[Coordinates, GeohashCentroid]
    transportation: TransportationFast
    travel_time: int
    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    snapping: Optional[Snapping] = None

    # JSON expects `"transportation": { "type": "public_transport" }` and not `"transportation": "public_transport"`
    @field_serializer('transportation')
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class GeoHashFastArrivalSearches(BaseModel):
    many_to_one: List[GeoHashFastSearch]
    one_to_many: List[GeoHashFastSearch]


class GeoHashFastRequest(TravelTimeRequest[GeoHashResponse]):
    resolution: int
    properties: List[CellProperty]
    arrival_searches: GeoHashFastArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            GeoHashFastRequest(
                resolution=self.resolution,
                properties=self.properties,
                arrival_searches=GeoHashFastArrivalSearches(
                    one_to_many=one_to_many, many_to_one=many_to_one
                ),
            )
            for one_to_many, many_to_one in split(
                self.arrival_searches.one_to_many,
                self.arrival_searches.many_to_one,
                window_size,
            )
        ]

    def merge(self, responses: List[GeoHashResponse]) -> GeoHashResponse:
        return GeoHashResponse(
            results=flatten([response.results for response in responses])
        )
