from typing import List

from geojson_pydantic import FeatureCollection
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.requests.time_map import (
    TimeMapDepartureSearch,
    TimeMapArrivalSearch,
)
from traveltimepy.itertools import split, flatten


class TimeMapGeojsonRequest(TravelTimeRequest[FeatureCollection]):
    departure_searches: List[TimeMapDepartureSearch]
    arrival_searches: List[TimeMapArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapGeojsonRequest(
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
