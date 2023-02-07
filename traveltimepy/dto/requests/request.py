from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')


class TravelTimeRequest(ABC, BaseModel, Generic[T]):
    @abstractmethod
    def split_searches(self) -> List[TravelTimeRequest]:
        pass

    @abstractmethod
    def merge(self, responses: List[T]) -> T:
        pass
