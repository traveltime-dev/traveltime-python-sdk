from typing import List

from geojson_pydantic import FeatureCollection
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.requests.time_map import (
    DepartureSearch,
    ArrivalSearch,
)
from traveltimepy.itertools import split, flatten


class TimeMapRequestGeojson(TravelTimeRequest[FeatureCollection]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapRequestGeojson(
                departure_searches=departures,
                arrival_searches=arrivals,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[FeatureCollection]) -> FeatureCollection:
        merged_features = flatten([response.features for response in responses])
        return FeatureCollection(type="FeatureCollection", features=merged_features)
