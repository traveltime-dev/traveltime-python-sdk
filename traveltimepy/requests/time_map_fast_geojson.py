from typing import List
from geojson_pydantic import FeatureCollection

from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.requests.time_map_fast import TimeMapFastArrivalSearches
from traveltimepy.itertools import split, flatten


class TimeMapFastGeojsonRequest(TravelTimeRequest[FeatureCollection]):
    arrival_searches: TimeMapFastArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapFastGeojsonRequest(
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

    def merge(self, responses: List[FeatureCollection]) -> FeatureCollection:
        merged_features = flatten([response.features for response in responses])
        return FeatureCollection(type="FeatureCollection", features=merged_features)
