from dataclasses import dataclass

from typing import NewType


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lng: float


SearchId = NewType('SearchId', str)
