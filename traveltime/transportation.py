from abc import ABC
from dataclasses import dataclass


@dataclass
class Transportation(ABC):
    type: str


@dataclass
class Driving(Transportation):
    type: str = 'Driving'

