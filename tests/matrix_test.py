from datetime import datetime, timedelta

import pytest

from traveltimepy.errors import TravelTimeJsonError
from traveltimepy.requests.common import Coordinates, Location, Property
from traveltimepy.requests.time_filter import TimeFilterArrivalSearch
from traveltimepy.requests.time_filter_fast import (
    TimeFilterFastArrivalSearches,
    TimeFilterFastOneToMany,
)
from traveltimepy.requests.time_filter_proto import (
    ProtoCountry,
    ProtoTransportation,
)
from traveltimepy.requests.transportation import DrivingFast, PublicTransport

LONDON = [
    Coordinates(lat=51.508930, lng=-0.131387),
    Coordinates(lat=51.508824, lng=-0.167093),
    Coordinates(lat=51.536067, lng=-0.153596),
    Coordinates(lat=51.503071, lng=-0.119469),
    Coordinates(lat=51.519470, lng=-0.126940),
]
SEA = Coordinates(lat=50.0, lng=-20.0)


def locations(origins, destinations):
    return [Location(id=f"o{i}", coords=c) for i, c in enumerate(origins)] + [
        Location(id=f"d{j}", coords=c) for j, c in enumerate(destinations)
    ]


def test_time_filter_fast_matrix(client):
    origins = LONDON[:2] + [SEA] + LONDON[2:3]
    destinations = LONDON

    matrix = client.time_filter_fast_matrix(
        origins, destinations, DrivingFast(), 3600, with_distance=True
    )

    (failure,) = matrix.failures
    assert failure.origins == range(2, 3)
    assert failure.destinations == range(len(destinations))
    assert isinstance(failure.error, TravelTimeJsonError)

    response = client.time_filter_fast(
        locations(origins, destinations),
        TimeFilterFastArrivalSearches(
            one_to_many=[
                TimeFilterFastOneToMany(
                    id=f"o{i}",
                    departure_location_id=f"o{i}",
                    arrival_location_ids=[f"d{j}" for j in range(len(destinations))],
                    transportation=DrivingFast(),
                    travel_time=3600,
                    properties=[Property.TRAVEL_TIME, Property.DISTANCE],
                )
                for i, c in enumerate(origins)
                if c != SEA
            ],
            many_to_one=[],
        ),
    )
    for result in response.results:
        origin = int(result.search_id[1:])
        for location in result.locations:
            destination = int(location.id[1:])
            assert matrix.travel_times[origin][destination] == (
                location.properties.travel_time
            )
            assert matrix.distances[origin][destination] == (
                location.properties.distance
            )
    assert matrix.travel_times[2] == [None] * len(destinations)


@pytest.mark.asyncio
async def test_time_filter_matrix(async_client):
    arrival_time = (datetime.now() + timedelta(days=7)).replace(hour=9, minute=0)
    origins = LONDON
    destinations = LONDON[:2]

    matrix = await async_client.time_filter_matrix(
        origins,
        destinations,
        PublicTransport(),
        3600,
        arrival_time=arrival_time,
        with_fares=True,
    )

    assert matrix.is_complete
    response = await async_client.time_filter(
        locations(origins, destinations),
        [],
        [
            TimeFilterArrivalSearch(
                id=f"d{j}",
                departure_location_ids=[f"o{i}" for i in range(len(origins))],
                arrival_location_id=f"d{j}",
                arrival_time=arrival_time,
                travel_time=3600,
                transportation=PublicTransport(),
                properties=[Property.TRAVEL_TIME],
            )
            for j in range(len(destinations))
        ],
    )
    for result in response.results:
        destination = int(result.search_id[1:])
        for location in result.locations:
            origin = int(location.id[1:])
            assert matrix.travel_times[origin][destination] == (
                location.properties[0].travel_time
            )
    assert any(fares is not None for row in matrix.fares for fares in row)


def test_time_filter_fast_proto_matrix(client):
    origins = LONDON[:3]
    destinations = LONDON + [SEA]

    matrix = client.time_filter_fast_proto_matrix(
        origins,
        destinations,
        ProtoTransportation.DRIVING_FERRY,
        3600,
        ProtoCountry.UNITED_KINGDOM,
        with_distance=True,
    )

    assert matrix.is_complete
    for i, origin in enumerate(origins):
        assert matrix.travel_times[i][-1] is None
        assert all(time is not None for time in matrix.travel_times[i][:-1])
        assert all(distance is not None for distance in matrix.distances[i][:-1])
