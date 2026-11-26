import asyncio
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from typing import Any, Dict, Generic, Optional, Tuple, Type, TypeVar

from tenacity import RetryError

from traveltimepy.base_client import BaseClient
from traveltimepy.errors import TravelTimeError
from traveltimepy.matrix.checkpoint import Checkpoint, PathLike
from traveltimepy.matrix.endpoints import MatrixEndpoint
from traveltimepy.matrix.plan import Search, max_batch_size, plan_searches
from traveltimepy.matrix.result import Matrix, MatrixBuilder, SearchResult
from traveltimepy.matrix.scheduler import MAX_CONCURRENCY, Batch, Scheduler

F = TypeVar("F")


def _request_errors(client: BaseClient) -> Tuple[Type[Exception], ...]:
    return (
        TravelTimeError,
        RetryError,
        *client._connection_errors,
        *client._timeout_errors,
    )


class _Job(Generic[F]):
    """Everything one matrix computation needs, shared by the sync and async drivers."""

    def __init__(
        self,
        endpoint: MatrixEndpoint[F],
        checkpoint: Optional[PathLike],
        resume_from: Optional[Matrix[F]],
    ):
        self.endpoint = endpoint
        fingerprint = endpoint.fingerprint()
        self.plan = plan_searches(
            len(endpoint.origins),
            len(endpoint.destinations),
            endpoint.max_points_per_search,
            endpoint.direction,
        )
        self.builder: MatrixBuilder[F] = MatrixBuilder(
            len(endpoint.origins),
            len(endpoint.destinations),
            self.plan.direction,
            endpoint.with_distance,
            endpoint.with_fares,
            fingerprint,
        )
        if resume_from is not None:
            if resume_from._fingerprint != fingerprint:
                raise ValueError("resume_from was computed for a different matrix")
            self.builder.restore(resume_from)

        self.checkpoint = (
            Checkpoint(checkpoint, fingerprint) if checkpoint is not None else None
        )
        if self.checkpoint is not None:
            searches = {search.id: search for search in self.plan.searches}
            for record in self.checkpoint.load():
                search = searches.get(record.get("search", ""))
                if search is not None:
                    self.builder.add(search, endpoint.from_record(record))

        done = self.builder.done
        pending = [search for search in self.plan.searches if search.id not in done]
        self.scheduler: Scheduler[F] = Scheduler(
            pending,
            max_batch_size(
                pending,
                endpoint.max_searches_per_request,
                endpoint.max_points_per_request,
            ),
            self._on_result,
            self.builder.fail,
        )
        if self.checkpoint is not None:
            self.checkpoint.open()

    def send(self, client: BaseClient, batch: Batch) -> Any:
        return self.endpoint.send(client, self.plan.direction, batch.searches)

    def succeeded(self, batch: Batch, response: Any) -> None:
        results = self.endpoint.parse(self.plan.direction, batch.searches, response)
        self.scheduler.succeeded(batch, results)

    def close(self) -> None:
        if self.checkpoint is not None:
            self.checkpoint.close()

    def _on_result(self, search: Search, result: SearchResult[F]) -> None:
        self.builder.add(search, result)
        if self.checkpoint is not None:
            self.checkpoint.append(self.endpoint.to_record(search, result))


def run_matrix(
    client: BaseClient,
    endpoint: MatrixEndpoint[F],
    checkpoint: Optional[PathLike],
    resume_from: Optional[Matrix[F]],
) -> Matrix[F]:
    job = _Job(endpoint, checkpoint, resume_from)
    scheduler = job.scheduler
    errors = _request_errors(client)
    pool = ThreadPoolExecutor(max_workers=MAX_CONCURRENCY)
    in_flight: Dict["Future[Any]", Batch] = {}
    try:
        while not scheduler.finished:
            batch = scheduler.next_batch()
            while batch is not None:
                in_flight[pool.submit(job.send, client, batch)] = batch
                batch = scheduler.next_batch()
            done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
            for future in done:
                batch = in_flight.pop(future)
                try:
                    response = future.result()
                except errors as error:
                    scheduler.failed(batch, error)
                else:
                    job.succeeded(batch, response)
    finally:
        pool.shutdown(wait=False, cancel_futures=True)
        job.close()
    return job.builder.build()


async def run_matrix_async(
    client: BaseClient,
    endpoint: MatrixEndpoint[F],
    checkpoint: Optional[PathLike],
    resume_from: Optional[Matrix[F]],
) -> Matrix[F]:
    job = _Job(endpoint, checkpoint, resume_from)
    scheduler = job.scheduler
    errors = _request_errors(client)
    in_flight: Dict["asyncio.Future[Any]", Batch] = {}
    try:
        while not scheduler.finished:
            batch = scheduler.next_batch()
            while batch is not None:
                in_flight[asyncio.ensure_future(job.send(client, batch))] = batch
                batch = scheduler.next_batch()
            done, _ = await asyncio.wait(in_flight, return_when=FIRST_COMPLETED)
            for task in done:
                batch = in_flight.pop(task)
                try:
                    response = task.result()
                except errors as error:
                    scheduler.failed(batch, error)
                else:
                    job.succeeded(batch, response)
    finally:
        for task in in_flight:
            task.cancel()
        job.close()
    return job.builder.build()
