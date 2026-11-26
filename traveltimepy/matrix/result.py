from dataclasses import dataclass, field
from typing import FrozenSet, Generic, List, Optional, Set, TypeVar

from traveltimepy.matrix.plan import Direction, Search

F = TypeVar("F")

Grid = List[List[Optional[int]]]


@dataclass
class SearchResult(Generic[F]):
    """Values for one search, aligned with its slice; None where unreachable."""

    travel_times: List[Optional[int]]
    distances: Optional[List[Optional[int]]]
    fares: Optional[List[Optional[F]]]


@dataclass
class MatrixFailure:
    """A block of the matrix that wasn't computed.

    Attributes:
        origins: Origin indices of the block
        destinations: Destination indices of the block
        error: Why the block wasn't computed
    """

    origins: range
    destinations: range
    error: Exception


@dataclass
class Matrix(Generic[F]):
    """Travel time matrix, indexed as [origin][destination] in input order.

    Cells are None where the destination is unreachable or the cell wasn't computed;
    `failures` lists the cells that weren't computed.

    Attributes:
        travel_times: Travel times in seconds
        distances: Distances in meters, if requested
        fares: Fares, if requested
        failures: Blocks that weren't computed. Pass the matrix as `resume_from` to
            compute just these.
    """

    travel_times: Grid
    distances: Optional[Grid]
    fares: Optional[List[List[Optional[F]]]]
    failures: List[MatrixFailure]
    _fingerprint: str = field(repr=False)
    _done: FrozenSet[str] = field(repr=False)

    @property
    def is_complete(self) -> bool:
        return not self.failures


def _grid(origins: int, destinations: int) -> List[List[Optional[F]]]:
    return [[None] * destinations for _ in range(origins)]


class MatrixBuilder(Generic[F]):
    def __init__(
        self,
        origins: int,
        destinations: int,
        direction: Direction,
        with_distance: bool,
        with_fares: bool,
        fingerprint: str,
    ):
        self._direction = direction
        self._fingerprint = fingerprint
        self._travel_times: Grid = _grid(origins, destinations)
        self._distances: Optional[Grid] = (
            _grid(origins, destinations) if with_distance else None
        )
        self._fares: Optional[List[List[Optional[F]]]] = (
            _grid(origins, destinations) if with_fares else None
        )
        self._failures: List[MatrixFailure] = []
        self._done: Set[str] = set()

    @property
    def done(self) -> FrozenSet[str]:
        return frozenset(self._done)

    def restore(self, matrix: Matrix[F]) -> None:
        self._travel_times = [row[:] for row in matrix.travel_times]
        if matrix.distances is not None:
            self._distances = [row[:] for row in matrix.distances]
        if matrix.fares is not None:
            self._fares = [row[:] for row in matrix.fares]
        self._done |= matrix._done

    def add(self, search: Search, result: SearchResult[F]) -> None:
        self._fill(self._travel_times, search, result.travel_times)
        if self._distances is not None and result.distances is not None:
            self._fill(self._distances, search, result.distances)
        if self._fares is not None and result.fares is not None:
            self._fill(self._fares, search, result.fares)
        self._done.add(search.id)

    def fail(self, search: Search, error: Exception) -> None:
        anchor = range(search.anchor, search.anchor + 1)
        others = range(search.start, search.end)
        origins, destinations = (
            (anchor, others)
            if self._direction == Direction.ONE_TO_MANY
            else (others, anchor)
        )
        self._failures.append(MatrixFailure(origins, destinations, error))

    def _fill(self, grid: List[List], search: Search, values: List) -> None:
        if self._direction == Direction.ONE_TO_MANY:
            grid[search.anchor][search.start : search.end] = values
        else:
            for origin, value in zip(range(search.start, search.end), values):
                grid[origin][search.anchor] = value

    def build(self) -> Matrix[F]:
        return Matrix(
            travel_times=self._travel_times,
            distances=self._distances,
            fares=self._fares,
            failures=self._failures,
            _fingerprint=self._fingerprint,
            _done=frozenset(self._done),
        )
