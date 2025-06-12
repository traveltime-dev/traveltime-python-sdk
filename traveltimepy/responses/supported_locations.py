from typing import List

from pydantic import BaseModel


class SupportedLocation(BaseModel):
    id: str
    map_name: str
    additional_map_names: List[str]


class SupportedLocationsResponse(BaseModel):
    locations: List[SupportedLocation]
    unsupported_locations: List[str]
