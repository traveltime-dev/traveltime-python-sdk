import itertools
from enum import Enum

from pydantic import BaseModel
from typing import TypeVar, Dict, List


class Rectangle(BaseModel):
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float


class Property(str, Enum):
    TRAVEL_TIME = 'travel_time'
    DISTANCE = 'distance'
    ROUTE = 'route'
    FARES = 'fares'


class FullRange(BaseModel):
    enabled: bool
    max_results: int
    width: int


class Range(BaseModel):
    enabled: bool
    width: int


T = TypeVar('T')


def flatten(list_of_lists: List[List[T]]):
    return list(itertools.chain.from_iterable(list_of_lists))


def to_list(values: Dict[T, List[T]]) -> List[T]:
    return flatten([[k] + v for k, v in values.items()])
