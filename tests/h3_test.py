from datetime import datetime

import pytest

from traveltimepy import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Coordinates, H3Centroid, CellProperty, Range
from traveltimepy.requests.h3 import (
    H3DepartureSearch,
    H3ArrivalSearch,
    H3Union,
    H3Intersection,
)
from traveltimepy.requests.transportation import Driving


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient):
    response = await async_client.h3(
        arrival_searches=[],
        departure_searches=[
            H3DepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
            H3DepartureSearch(
                id="id 2",
                coords=H3Centroid(h3_centroid="87195da49ffffff"),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=7,
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient):
    response = await async_client.h3(
        departure_searches=[],
        arrival_searches=[
            H3ArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
            H3ArrivalSearch(
                id="id 2",
                coords=H3Centroid(h3_centroid="87195da49ffffff"),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=7,
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_union_departures(async_client: AsyncClient):
    response = await async_client.h3(
        arrival_searches=[],
        departure_searches=[
            H3DepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
            H3DepartureSearch(
                id="id 2",
                coords=H3Centroid(h3_centroid="87195da49ffffff"),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=7,
        unions=[H3Union(id="union", search_ids=["id", "id 2"])],
    )

    assert len(response.results) == 3


@pytest.mark.asyncio
async def test_intersection_arrivals(async_client: AsyncClient):
    response = await async_client.h3(
        departure_searches=[],
        arrival_searches=[
            H3ArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
            H3ArrivalSearch(
                id="id 2",
                coords=H3Centroid(h3_centroid="87195da49ffffff"),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=7,
        intersections=[H3Intersection(id="intersection", search_ids=["id", "id 2"])],
    )

    assert len(response.results) == 3


def test_departures_sync(client: Client):
    response = client.h3(
        arrival_searches=[],
        departure_searches=[
            H3DepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
            H3DepartureSearch(
                id="id 2",
                coords=H3Centroid(h3_centroid="87195da49ffffff"),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=7,
    )

    assert len(response.results) == 2


def test_arrivals_sync(client: Client):
    response = client.h3(
        departure_searches=[],
        arrival_searches=[
            H3ArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
            H3ArrivalSearch(
                id="id 2",
                coords=H3Centroid(h3_centroid="87195da49ffffff"),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=7,
    )

    assert len(response.results) == 2


def test_union_departures_sync(client: Client):
    response = client.h3(
        arrival_searches=[],
        departure_searches=[
            H3DepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
            H3DepartureSearch(
                id="id 2",
                coords=H3Centroid(h3_centroid="87195da49ffffff"),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=7,
        unions=[H3Union(id="union", search_ids=["id", "id 2"])],
    )

    assert len(response.results) == 3


def test_intersection_arrivals_sync(client: Client):
    response = client.h3(
        departure_searches=[],
        arrival_searches=[
            H3ArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
            H3ArrivalSearch(
                id="id 2",
                coords=H3Centroid(h3_centroid="87195da49ffffff"),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=7,
        intersections=[H3Intersection(id="intersection", search_ids=["id", "id 2"])],
    )

    assert len(response.results) == 3


def test_no_properties_requested_sync(client: Client):
    response = client.h3(
        arrival_searches=[],
        departure_searches=[
            H3DepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=600,
                transportation=Driving(),
            )
        ],
        properties=[],
        resolution=8,
    )

    assert len(response.results[0].cells) > 0
    assert all(cell.properties is None for cell in response.results[0].cells)


def test_remove_water_bodies_drops_cells_over_the_thames_sync(client: Client):
    def cells(remove_water_bodies):
        response = client.h3(
            arrival_searches=[],
            departure_searches=[
                H3DepartureSearch(
                    id="id",
                    coords=Coordinates(lat=51.5066, lng=-0.1176),
                    departure_time=datetime.now(),
                    travel_time=600,
                    transportation=Driving(),
                    remove_water_bodies=remove_water_bodies,
                )
            ],
            properties=[CellProperty.MEAN],
            resolution=10,
        )
        return {cell.id for cell in response.results[0].cells}

    with_water, without_water = cells(False), cells(True)
    assert without_water < with_water
