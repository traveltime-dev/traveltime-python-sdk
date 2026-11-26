from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, Generic, List, Optional, TypeVar

from traveltimepy.base_client import _is_rate_limited
from traveltimepy.errors import TravelTimeApiError
from traveltimepy.matrix.plan import Search
from traveltimepy.matrix.result import SearchResult

F = TypeVar("F")

MAX_CONCURRENCY = 10


@dataclass(frozen=True)
class Batch:
    searches: List[Search]
    generation: int


def _chunks(searches: List[Search], size: int) -> List[List[Search]]:
    return [searches[i : i + size] for i in range(0, len(searches), size)]


def _is_rejected(error: Exception) -> bool:
    return isinstance(error, TravelTimeApiError) and 400 <= error.status_code < 500


class Scheduler(Generic[F]):
    """Decides which searches to send next and how to react to failed requests, without
    doing any IO.

    Errors reaching here have already been retried by the client:
    - Rate limited: the request may cost more than the plan allows per minute, or
      too many are in flight, so both batch size and concurrency are halved and the
      batch is sent again. Once a single search sent alone is still rate limited, the
      run stops.
    - Rejected (other 4xx): usually one search with a bad location, so the batch is
      halved until the failing search is isolated and recorded as failed.
    - Anything else (5xx, connection failures): the run stops.

    After a stop, in-flight batches still complete and everything unsent is recorded
    as failed with the error that caused the stop.
    """

    def __init__(
        self,
        searches: List[Search],
        max_batch_size: int,
        on_result: Callable[[Search, SearchResult[F]], None],
        on_failure: Callable[[Search, Exception], None],
    ):
        self._queue: Deque[List[Search]] = deque(_chunks(searches, max_batch_size))
        self._batch_size = max_batch_size
        self._concurrency = MAX_CONCURRENCY
        self._generation = 0
        self._in_flight = 0
        self._stop_error: Optional[Exception] = None
        self._on_result = on_result
        self._on_failure = on_failure

    @property
    def finished(self) -> bool:
        stopped_or_drained = self._stop_error is not None or not self._queue
        return self._in_flight == 0 and stopped_or_drained

    def next_batch(self) -> Optional[Batch]:
        if self._stop_error is not None or not self._queue:
            return None
        if self._in_flight >= self._concurrency:
            return None
        searches = self._queue.popleft()
        if len(searches) > self._batch_size:
            self._requeue(_chunks(searches[self._batch_size :], self._batch_size))
            searches = searches[: self._batch_size]
        self._in_flight += 1
        return Batch(searches, self._generation)

    def succeeded(self, batch: Batch, results: List[SearchResult[F]]) -> None:
        self._in_flight -= 1
        for search, result in zip(batch.searches, results):
            self._on_result(search, result)

    def failed(self, batch: Batch, error: Exception) -> None:
        self._in_flight -= 1
        if self._stop_error is not None:
            for search in batch.searches:
                self._on_failure(search, error)
        elif _is_rate_limited(error):
            self._rate_limited(batch, error)
        elif _is_rejected(error) and len(batch.searches) > 1:
            middle = len(batch.searches) // 2
            self._requeue([batch.searches[:middle], batch.searches[middle:]])
        elif _is_rejected(error):
            self._on_failure(batch.searches[0], error)
        else:
            self._stop(batch, error)

    def _rate_limited(self, batch: Batch, error: Exception) -> None:
        if batch.generation == self._generation:
            if self._concurrency == 1 and len(batch.searches) == 1:
                self._stop(batch, error)
                return
            self._concurrency = max(1, self._concurrency // 2)
            self._batch_size = max(1, self._batch_size // 2)
            self._generation += 1
        self._requeue([batch.searches])

    def _stop(self, batch: Batch, error: Exception) -> None:
        if self._stop_error is None:
            self._stop_error = error
        for search in batch.searches:
            self._on_failure(search, error)
        while self._queue:
            for search in self._queue.popleft():
                self._on_failure(search, self._stop_error)

    def _requeue(self, batches: List[List[Search]]) -> None:
        self._queue.extendleft(reversed(batches))
