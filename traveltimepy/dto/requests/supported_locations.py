from typing import List

from traveltimepy.dto.common import Location
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.supported_locations import SupportedLocationsResponse
from traveltimepy.itertools import flatten


class SupportedLocationsRequest(TravelTimeRequest[SupportedLocationsResponse]):
    locations: List[Location]

    def split_searches(self) -> List[TravelTimeRequest]:
        return [SupportedLocationsRequest(locations=self.locations)]

    def merge(self, responses: List[SupportedLocationsResponse]) -> SupportedLocationsResponse:
        return SupportedLocationsResponse(
            locations=flatten([response.locations for response in responses]),
            unsupported_locations=flatten([response.unsupported_locations for response in responses])
        )
