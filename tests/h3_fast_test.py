import pytest

from traveltimepy import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Coordinates, H3Centroid, CellProperty
from traveltimepy.requests.h3_fast import H3FastArrivalSearches, H3FastSearch
from traveltimepy.requests.transportation import TransportationFast


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient):
    response = await async_client.h3_fast(
        arrival_searches=H3FastArrivalSearches(
            one_to_many=[
                H3FastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                H3FastSearch(
                    id="id 2",
                    coords=H3Centroid(h3_centroid="87195da49ffffff"),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        ),
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient):
    response = await async_client.h3_fast(
        arrival_searches=H3FastArrivalSearches(
            many_to_one=[
                H3FastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                H3FastSearch(
                    id="id 2",
                    coords=H3Centroid(h3_centroid="87195da49ffffff"),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        ),
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
    )

    assert len(response.results) == 2


def test_one_to_many_sync(client: Client):
    response = client.h3_fast(
        arrival_searches=H3FastArrivalSearches(
            one_to_many=[
                H3FastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                H3FastSearch(
                    id="id 2",
                    coords=H3Centroid(h3_centroid="87195da49ffffff"),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        ),
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
    )

    assert len(response.results) == 2


def test_many_to_one_sync(client: Client):
    response = client.h3_fast(
        arrival_searches=H3FastArrivalSearches(
            many_to_one=[
                H3FastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                H3FastSearch(
                    id="id 2",
                    coords=H3Centroid(h3_centroid="87195da49ffffff"),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        ),
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
    )

    assert len(response.results) == 2
