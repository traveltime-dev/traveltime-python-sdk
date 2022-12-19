from typing import List, Optional

from pydantic import BaseModel

from traveltimepy.dto import SearchId


class TravelTime(BaseModel):
    min: int
    max: int
    mean: int
    median: int


class Properties(BaseModel):
    travel_time_reachable: Optional[TravelTime]
    travel_time_all: Optional[TravelTime]
    coverage: Optional[float]


class Zone(BaseModel):
    code: str
    properties: Properties


class SectorsResult(BaseModel):
    search_id: SearchId
    sectors: List[Zone]


class DistrictsResult(BaseModel):
    search_id: SearchId
    districts: List[Zone]


class SectorsResponse(BaseModel):
    results: List[SectorsResult]


class DistrictsResponse(BaseModel):
    results: List[DistrictsResult]
