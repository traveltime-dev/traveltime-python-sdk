import pytest

from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Coordinates
from traveltimepy.requests.time_map_fast import (
    TimeMapFastArrivalSearches,
    TimeMapFastSearch,
)
from traveltimepy.requests.transportation import TransportationFast


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient):
    response = await async_client.time_map_fast(
        arrival_searches=TimeMapFastArrivalSearches(
            one_to_many=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        )
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient):
    response = await async_client.time_map_fast(
        arrival_searches=TimeMapFastArrivalSearches(
            many_to_one=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        )
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_one_to_many_geojson(async_client: AsyncClient):
    response = await async_client.time_map_fast_geojson(
        arrival_searches=TimeMapFastArrivalSearches(
            one_to_many=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        )
    )

    assert len(response.features) == 2


@pytest.mark.asyncio
async def test_many_to_one_geojson(async_client: AsyncClient):
    response = await async_client.time_map_fast_geojson(
        arrival_searches=TimeMapFastArrivalSearches(
            many_to_one=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        )
    )

    assert len(response.features) == 2


@pytest.mark.asyncio
async def test_one_to_many_wkt(async_client: AsyncClient):
    response = await async_client.time_map_fast_wkt(
        arrival_searches=TimeMapFastArrivalSearches(
            one_to_many=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        )
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_many_to_one_wkt(async_client: AsyncClient):
    response = await async_client.time_map_fast_wkt(
        arrival_searches=TimeMapFastArrivalSearches(
            many_to_one=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        )
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_one_to_many_wkt_no_holes(async_client: AsyncClient):
    response = await async_client.time_map_fast_wkt_no_holes(
        arrival_searches=TimeMapFastArrivalSearches(
            one_to_many=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        )
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_many_to_one_wkt_no_holes(async_client: AsyncClient):
    response = await async_client.time_map_fast_wkt_no_holes(
        arrival_searches=TimeMapFastArrivalSearches(
            many_to_one=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        )
    )

    assert len(response.results) == 2


def test_one_to_many_sync(client: Client):
    response = client.time_map_fast(
        arrival_searches=TimeMapFastArrivalSearches(
            one_to_many=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        )
    )

    assert len(response.results) == 2


def test_many_to_one_sync(client: Client):
    response = client.time_map_fast(
        arrival_searches=TimeMapFastArrivalSearches(
            many_to_one=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        )
    )

    assert len(response.results) == 2


def test_one_to_many_geojson_sync(client: Client):
    response = client.time_map_fast_geojson(
        arrival_searches=TimeMapFastArrivalSearches(
            one_to_many=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        )
    )

    assert len(response.features) == 2


def test_many_to_one_geojson_sync(client: Client):
    response = client.time_map_fast_geojson(
        arrival_searches=TimeMapFastArrivalSearches(
            many_to_one=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        )
    )

    assert len(response.features) == 2


def test_one_to_many_wkt_sync(client: Client):
    response = client.time_map_fast_wkt(
        arrival_searches=TimeMapFastArrivalSearches(
            one_to_many=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        )
    )

    assert len(response.results) == 2


def test_many_to_one_wkt_sync(client: Client):
    response = client.time_map_fast_wkt(
        arrival_searches=TimeMapFastArrivalSearches(
            many_to_one=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        )
    )

    assert len(response.results) == 2


def test_one_to_many_wkt_no_holes_sync(client: Client):
    response = client.time_map_fast_wkt_no_holes(
        arrival_searches=TimeMapFastArrivalSearches(
            one_to_many=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        )
    )

    assert len(response.results) == 2


def test_many_to_one_wkt_no_holes_sync(client: Client):
    response = client.time_map_fast_wkt_no_holes(
        arrival_searches=TimeMapFastArrivalSearches(
            many_to_one=[
                TimeMapFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                TimeMapFastSearch(
                    id="id 2",
                    coords=Coordinates(lat=51.517609, lng=-0.138315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        )
    )

    assert len(response.results) == 2
