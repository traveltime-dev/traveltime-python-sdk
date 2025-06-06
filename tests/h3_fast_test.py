import pytest

from traveltimepy import TransportationFast
from traveltimepy.async_client import AsyncClient
from traveltimepy.dto.common import CellProperty, Coordinates, H3Centroid
from traveltimepy.dto.requests.h3_fast import H3FastArrivalSearches, H3FastSearch


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient):
    results = await async_client.h3_fast(
        arrival_searches=H3FastArrivalSearches(
            one_to_many=[
                H3FastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast(type="public_transport"),
                    travel_time=900
                ),
                H3FastSearch(
                    id="id 2",
                    coords=H3Centroid(h3_centroid="87195da49ffffff"),
                    transportation=TransportationFast(type="public_transport"),
                    travel_time=900
                ),
            ],
            many_to_one=[],
        ),
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN]
    )

    assert len(results) == 2


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient):
    results = await async_client.h3_fast(
        arrival_searches=H3FastArrivalSearches(
            many_to_one=[
                H3FastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast(type="public_transport"),
                    travel_time=900
                ),
                H3FastSearch(
                    id="id 2",
                    coords=H3Centroid(h3_centroid="87195da49ffffff"),
                    transportation=TransportationFast(type="public_transport"),
                    travel_time=900
                ),
            ],
            one_to_many=[],
        ),
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN]
    )

    assert len(results) == 2
