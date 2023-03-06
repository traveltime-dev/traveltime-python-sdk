from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class TravelTimeRequest(ABC, BaseModel, Generic[T]):
    @abstractmethod
    def split_searches(self) -> List[TravelTimeRequest]:
        pass

    @abstractmethod
    def merge(self, responses: List[T]) -> T:
        pass

    @property
    def api_hits_count(self) -> int:
        """Return the number of hits the API will count when sending this request."""
        return 1  # default value to avoid breaking existing code
