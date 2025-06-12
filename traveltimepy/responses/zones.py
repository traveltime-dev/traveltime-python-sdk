from typing import List, Optional

from pydantic import BaseModel


class TravelTime(BaseModel):
    min: int
    max: int
    mean: int
    median: int


class Properties(BaseModel):
    travel_time_reachable: Optional[TravelTime] = None
    travel_time_all: Optional[TravelTime] = None
    coverage: Optional[float] = None


class Zone(BaseModel):
    code: str
    properties: Properties


class PostcodesSectorsResult(BaseModel):
    search_id: str
    sectors: List[Zone]


class PostcodesDistrictsResult(BaseModel):
    search_id: str
    districts: List[Zone]


class PostcodesSectorsResponse(BaseModel):
    results: List[PostcodesSectorsResult]


class PostcodesDistrictsResponse(BaseModel):
    results: List[PostcodesDistrictsResult]
