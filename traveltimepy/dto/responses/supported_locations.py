from typing import List

from pydantic import BaseModel

from traveltimepy.dto import LocationId


class Location(BaseModel):
    id: LocationId
    map_name: str
    additional_map_names: List[str]


class SupportedLocationsResponse(BaseModel):
    locations: List[Location]
    unsupported_locations: List[LocationId]
