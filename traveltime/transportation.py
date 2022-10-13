from abc import ABC
from dataclasses import dataclass


@dataclass
class Transportation(ABC):

@dataclass
class Driving(Transportation):
    type: str = 'driving'

