from dataclasses import dataclass
from typing import List

from traveltime import SearchId, Coordinate


@dataclass(frozen=True)
class Shape:
    shell: List[Coordinate]
    holes: List[List[Coordinate]]


@dataclass(frozen=True)
class Result:
    search_id: SearchId
    shapes: List[Shape]


@dataclass(frozen=True)
class TimeMapResponse:
    results: List[Result]

@dataclass(frozen=True)
class Map:
    name: str

@dataclass(frozen=True)
class MapInfo:
    maps: List[Map]



