from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Direction(str, Enum):
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"


@dataclass(frozen=True)
class Search:
    """One API search: a single anchor location against a contiguous slice of the other
    side.

    For ONE_TO_MANY the anchor is an origin index and the slice covers destinations, for
    MANY_TO_ONE it is the other way around.
    """

    anchor: int
    start: int
    end: int

    @property
    def id(self) -> str:
        return f"{self.anchor}:{self.start}-{self.end}"


@dataclass(frozen=True)
class Plan:
    direction: Direction
    searches: List[Search]


def _search_count(anchors: int, others: int, max_points: int) -> int:
    return anchors * -(-others // max_points)


def plan_searches(
    origins: int,
    destinations: int,
    max_points: int,
    direction: Optional[Direction],
) -> Plan:
    """Split an origins x destinations matrix into searches.

    Without a fixed direction, the one needing fewer searches is used, with ONE_TO_MANY
    winning ties.
    """
    if direction is None:
        one_to_many = _search_count(origins, destinations, max_points)
        many_to_one = _search_count(destinations, origins, max_points)
        direction = (
            Direction.MANY_TO_ONE
            if many_to_one < one_to_many
            else Direction.ONE_TO_MANY
        )

    anchors, others = (
        (origins, destinations)
        if direction == Direction.ONE_TO_MANY
        else (destinations, origins)
    )
    return Plan(
        direction=direction,
        searches=[
            Search(anchor, start, min(start + max_points, others))
            for anchor in range(anchors)
            for start in range(0, others, max_points)
        ],
    )


def max_batch_size(
    searches: List[Search], max_searches_per_request: int, max_points_per_request: int
) -> int:
    longest = max((search.end - search.start for search in searches), default=1)
    return max(1, min(max_searches_per_request, max_points_per_request // longest))
