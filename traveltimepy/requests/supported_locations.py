from typing import List

from traveltimepy.requests.common import Location
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.supported_locations import SupportedLocationsResponse
from traveltimepy.itertools import flatten


class SupportedLocationsRequest(TravelTimeRequest[SupportedLocationsResponse]):
    locations: List[Location]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [SupportedLocationsRequest(locations=self.locations)]

    def merge(
        self, responses: List[SupportedLocationsResponse]
    ) -> SupportedLocationsResponse:
        return SupportedLocationsResponse(
            locations=flatten([response.locations for response in responses]),
            unsupported_locations=flatten(
                [response.unsupported_locations for response in responses]
            ),
        )
