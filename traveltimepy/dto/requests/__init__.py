import itertools
from enum import Enum

from pydantic import BaseModel
from typing import TypeVar, Dict, List, Iterator


class Rectangle(BaseModel):
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float

    def to_str(self):
        return f'{self.min_lat},{self.min_lng},{self.max_lat},{self.max_lng}'


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




