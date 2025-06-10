import pytest

from traveltimepy import TransportationFast
from traveltimepy.async_client import AsyncClient
from traveltimepy.dto.common import (
    CellProperty,
    Coordinates,
    GeohashCentroid,
    ArrivalTimePeriod,
)
from traveltimepy.dto.requests.geohash_fast import (
    GeoHashFastArrivalSearches,
    GeoHashFastSearch,
)


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient):
    results = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(results) == 2


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient):
    results = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[],
            many_to_one=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=TransportationFast.PUBLIC_TRANSPORT,
                    travel_time=900,
                ),
            ],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(results) == 2
