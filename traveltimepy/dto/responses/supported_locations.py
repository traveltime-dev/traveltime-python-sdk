from typing import List

from pydantic import BaseModel

from traveltimepy.dto.common import LocationId


class SupportedLocation(BaseModel):
    id: LocationId
    map_name: str
    additional_map_names: List[str]


class SupportedLocationsResponse(BaseModel):
    locations: List[SupportedLocation]
    unsupported_locations: List[LocationId]
