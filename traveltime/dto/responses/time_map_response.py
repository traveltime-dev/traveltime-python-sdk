from dataclasses import dataclass
from typing import List

from traveltime.dto import SearchId, Coordinates


@dataclass(frozen=True)
class Shape:
    shell: List[Coordinates]
    holes: List[List[Coordinates]]


@dataclass(frozen=True)
class Result:
    search_id: SearchId
    shapes: List[Shape]


@dataclass(frozen=True)
class TimeMapResponse:
    results: List[Result]
