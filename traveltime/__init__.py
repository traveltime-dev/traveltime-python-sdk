from dataclasses import dataclass

from typing import NewType
from enum import Enum


class RequestType(Enum):
    GET = 1
    POST = 2


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lng: float


SearchId = NewType('SearchId', str)


