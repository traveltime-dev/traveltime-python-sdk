import asyncio
from typing import AbstractSet, Dict, List, Optional

import pytest

from traveltimepy.errors import TravelTimeJsonError, TravelTimeServerError
from traveltimepy.matrix.backends import TimeFilterFastBackend
from traveltimepy.matrix.plan import Search
from traveltimepy.matrix.runner import run_matrix, run_matrix_async
from traveltimepy.matrix.scheduler import MatrixRun
from traveltimepy.requests.common import ArrivalTimePeriod, Coordinates
from traveltimepy.requests.transportation import DrivingFast
from traveltimepy.responses.time_filter_fast import (
    Location,
    Properties,
    TimeFilterFastResponse,
    TimeFilterFastResult,
)


def api_error(status_code: int) -> TravelTimeJsonError:
    return TravelTimeJsonError(status_code, "9", "", "", {})


def searches(count: int) -> List[Search]:
    return [Search(anchor, 0, 1) for anchor in range(count)]


def new_run(count: int, max_batch_size: int):
    results: Dict[int, object] = {}
    failures: Dict[int, Exception] = {}
    run: MatrixRun[object] = MatrixRun(
        searches(count),
        max_batch_size,
        lambda search, result: results.__setitem__(search.anchor, result),
        lambda search, error: failures.__setitem__(search.anchor, error),
    )
    return run, results, failures


def drain(run: MatrixRun) -> list:
    batches = []
    while (batch := run.next_batch()) is not None:
        batches.append(batch)
    return batches


def test_rate_limited_batches_shrink_until_single_search_fails_alone():
    run, _, failures = new_run(count=20, max_batch_size=10)
    first, second = drain(run)

    run.failed(first, api_error(429))
    run.failed(second, api_error(429))

    batches = drain(run)
    assert [len(batch.searches) for batch in batches] == [5, 5, 5, 5]

    for limit in [2, 1]:
        for batch in batches:
            run.failed(batch, api_error(429))
        batches = drain(run)
        assert len(batches) == limit

    assert [len(batch.searches) for batch in batches] == [1]
    run.failed(batches[0], api_error(429))
    assert run.finished
    assert len(failures) == 20


def test_rejected_batch_is_split_until_the_bad_search_is_isolated():
    run, results, failures = new_run(count=10, max_batch_size=10)
    rejected = api_error(422)

    while not run.finished:
        for batch in drain(run):
            if any(search.anchor == 7 for search in batch.searches):
                run.failed(batch, rejected)
            else:
                run.succeeded(batch, [object()] * len(batch.searches))

    assert failures == {7: rejected}
    assert set(results) == set(range(10)) - {7}


def test_server_error_stops_the_run_but_in_flight_batches_finish():
    run, results, failures = new_run(count=30, max_batch_size=5)
    first, second, *rest = drain(run)
    error = TravelTimeServerError("boom")

    run.failed(first, error)
    assert run.next_batch() is None
    run.succeeded(second, [object()] * 5)
    for batch in rest:
        run.failed(batch, api_error(429))

    assert run.finished
    assert set(results) == set(range(5, 10))
    assert set(failures) == set(range(30)) - set(range(5, 10))
    assert failures[0] is error


ORIGINS = [Coordinates(lat=51.5, lng=-0.1 + i / 1000) for i in range(25)]
DESTINATIONS = [Coordinates(lat=51.6, lng=-0.1 + j / 1000) for j in range(30)]


def expected_time(origin: int, destination: int) -> Optional[int]:
    return None if (origin + destination) % 7 == 0 else origin * 100 + destination


class FakeClient:
    _connection_errors = (ConnectionError,)
    _timeout_errors = ()

    def __init__(self, failing_origins: AbstractSet[int] = frozenset()):
        self.failing_origins = failing_origins
        self.searches_sent = 0

    def respond(self, arrival_searches) -> TimeFilterFastResponse:
        results = []
        for search in arrival_searches.one_to_many:
            origin = int(search.departure_location_id[1:])
            if origin in self.failing_origins:
                raise ConnectionError("connection dropped")
            reachable = [
                (location_id, expected_time(origin, int(location_id[1:])))
                for location_id in search.arrival_location_ids
            ]
            results.append(
                TimeFilterFastResult(
                    search_id=search.id,
                    locations=[
                        Location(
                            id=location_id, properties=Properties(travel_time=time)
                        )
                        for location_id, time in reachable
                        if time is not None
                    ],
                    unreachable=[
                        location_id for location_id, time in reachable if time is None
                    ],
                )
            )
        self.searches_sent += len(results)
        return TimeFilterFastResponse(results=results)

    def time_filter_fast(self, locations, arrival_searches):
        return self.respond(arrival_searches)


class AsyncFakeClient(FakeClient):
    async def time_filter_fast(self, locations, arrival_searches):
        await asyncio.sleep(0)
        return self.respond(arrival_searches)


def backend(origins=ORIGINS):
    return TimeFilterFastBackend(
        origins,
        DESTINATIONS,
        False,
        False,
        DrivingFast(),
        3600,
        ArrivalTimePeriod.WEEKDAY_MORNING,
        None,
    )


def run(client_class, checkpoint=None, resume_from=None, **client_args):
    client = client_class(**client_args)
    if client_class is AsyncFakeClient:
        matrix = asyncio.run(
            run_matrix_async(client, backend(), checkpoint, resume_from)
        )
    else:
        matrix = run_matrix(client, backend(), checkpoint, resume_from)
    return matrix, client


def expected_matrix() -> List[List[Optional[int]]]:
    return [
        [expected_time(origin, destination) for destination in range(len(DESTINATIONS))]
        for origin in range(len(ORIGINS))
    ]


@pytest.fixture(params=[FakeClient, AsyncFakeClient], ids=["sync", "async"])
def client_class(request):
    return request.param


def test_dropped_connection_returns_partial_matrix_and_checkpoint_resumes(
    client_class, tmp_path
):
    checkpoint = tmp_path / "matrix.jsonl"

    partial, _ = run(client_class, checkpoint, failing_origins={12})

    assert not partial.is_complete
    failed_origins = {i for failure in partial.failures for i in failure.origins}
    assert failed_origins == set(range(10, 20))
    assert partial.travel_times[:10] == expected_matrix()[:10]
    assert partial.travel_times[12] == [None] * len(DESTINATIONS)

    resumed, client = run(client_class, checkpoint)

    assert resumed.is_complete
    assert resumed.travel_times == expected_matrix()
    assert client.searches_sent == 10


def test_resume_from_computes_only_failed_cells(client_class):
    partial, _ = run(client_class, failing_origins={3})

    resumed, client = run(client_class, resume_from=partial)

    assert resumed.is_complete
    assert resumed.travel_times == expected_matrix()
    assert client.searches_sent == 10


def test_checkpoint_skips_torn_last_line(tmp_path):
    checkpoint = tmp_path / "matrix.jsonl"
    run(FakeClient, checkpoint)
    lines = checkpoint.read_bytes().splitlines(keepends=True)
    checkpoint.write_bytes(b"".join(lines[:-1]) + lines[-1][:20])

    resumed, client = run(FakeClient, checkpoint)

    assert resumed.travel_times == expected_matrix()
    assert client.searches_sent == 1
    assert run(FakeClient, checkpoint)[1].searches_sent == 0


def test_checkpoint_for_other_inputs_is_rejected(tmp_path):
    checkpoint = tmp_path / "matrix.jsonl"
    run(FakeClient, checkpoint)

    with pytest.raises(ValueError, match="different matrix"):
        run_matrix(FakeClient(), backend(ORIGINS[:-1]), checkpoint, None)
