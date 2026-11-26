import asyncio
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from typing import Any, Dict, Generic, Optional, Tuple, Type, TypeVar

from tenacity import RetryError

from traveltimepy.base_client import BaseClient
from traveltimepy.errors import TravelTimeError
from traveltimepy.matrix.backends import MatrixBackend
from traveltimepy.matrix.checkpoint import Checkpoint, PathLike
from traveltimepy.matrix.plan import Search, max_batch_size, plan_searches
from traveltimepy.matrix.result import Matrix, MatrixBuilder, SearchResult
from traveltimepy.matrix.scheduler import MAX_CONCURRENCY, Batch, MatrixRun

F = TypeVar("F")


def _request_errors(client: BaseClient) -> Tuple[Type[Exception], ...]:
    return (
        TravelTimeError,
        RetryError,
        *client._connection_errors,
        *client._timeout_errors,
    )


class _Job(Generic[F]):
    def __init__(
        self,
        backend: MatrixBackend[F],
        checkpoint: Optional[PathLike],
        resume_from: Optional[Matrix[F]],
    ):
        self.backend = backend
        fingerprint = backend.fingerprint()
        self.plan = plan_searches(
            len(backend.origins),
            len(backend.destinations),
            backend.max_points_per_search,
            backend.direction,
        )
        self.builder: MatrixBuilder[F] = MatrixBuilder(
            len(backend.origins),
            len(backend.destinations),
            self.plan.direction,
            backend.with_distance,
            backend.with_fares,
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
                    self.builder.add(search, backend.from_record(record))

    def __enter__(self) -> MatrixRun[F]:
        if self.checkpoint is not None:
            self.checkpoint.__enter__()
        done = self.builder.done
        pending = [search for search in self.plan.searches if search.id not in done]
        return MatrixRun(
            pending,
            max_batch_size(
                pending,
                self.backend.max_searches_per_request,
                self.backend.max_points_per_request,
            ),
            self._on_result,
            self.builder.fail,
        )

    def __exit__(self, *exc_info: Any) -> None:
        if self.checkpoint is not None:
            self.checkpoint.__exit__(*exc_info)

    def _on_result(self, search: Search, result: SearchResult[F]) -> None:
        self.builder.add(search, result)
        if self.checkpoint is not None:
            self.checkpoint.append(self.backend.to_record(search, result))

    def succeeded(self, run: MatrixRun[F], batch: Batch, response: Any) -> None:
        run.succeeded(
            batch, self.backend.parse(self.plan.direction, batch.searches, response)
        )


def run_matrix(
    client: BaseClient,
    backend: MatrixBackend[F],
    checkpoint: Optional[PathLike],
    resume_from: Optional[Matrix[F]],
) -> Matrix[F]:
    job = _Job(backend, checkpoint, resume_from)
    errors = _request_errors(client)
    pool = ThreadPoolExecutor(max_workers=MAX_CONCURRENCY)
    try:
        with job as run:
            in_flight: Dict["Future[Any]", Batch] = {}
            while not run.finished:
                batch = run.next_batch()
                while batch is not None:
                    future = pool.submit(
                        backend.send, client, job.plan.direction, batch.searches
                    )
                    in_flight[future] = batch
                    batch = run.next_batch()
                done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
                for future in done:
                    batch = in_flight.pop(future)
                    try:
                        response = future.result()
                    except errors as error:
                        run.failed(batch, error)
                    else:
                        job.succeeded(run, batch, response)
    finally:
        pool.shutdown(wait=False, cancel_futures=True)
    return job.builder.build()


async def run_matrix_async(
    client: BaseClient,
    backend: MatrixBackend[F],
    checkpoint: Optional[PathLike],
    resume_from: Optional[Matrix[F]],
) -> Matrix[F]:
    job = _Job(backend, checkpoint, resume_from)
    errors = _request_errors(client)
    in_flight: Dict["asyncio.Future[Any]", Batch] = {}
    try:
        with job as run:
            while not run.finished:
                batch = run.next_batch()
                while batch is not None:
                    task = asyncio.ensure_future(
                        backend.send(client, job.plan.direction, batch.searches)
                    )
                    in_flight[task] = batch
                    batch = run.next_batch()
                done, _ = await asyncio.wait(in_flight, return_when=FIRST_COMPLETED)
                for task in done:
                    batch = in_flight.pop(task)
                    try:
                        response = task.result()
                    except errors as error:
                        run.failed(batch, error)
                    else:
                        job.succeeded(run, batch, response)
    finally:
        for task in in_flight:
            task.cancel()
    return job.builder.build()
