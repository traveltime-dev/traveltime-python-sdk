import pytest

from traveltimepy import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Coordinates, GeohashCentroid, CellProperty
from traveltimepy.requests.geohash_fast import (
    GeoHashFastSearch,
    GeoHashFastArrivalSearches,
)
from traveltimepy.requests.transportation import TransportationFast, FastTrafficModel


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient):
    response = await async_client.geohash_fast(
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

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient):
    response = await async_client.geohash_fast(
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

    assert len(response.results) == 2


def test_one_to_many_sync(client: Client):
    response = client.geohash_fast(
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

    assert len(response.results) == 2


def test_many_to_one_sync(client: Client):
    response = client.geohash_fast(
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

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_one_to_many_with_traffic_model(async_client: AsyncClient):
    response = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.DRIVING,
                    travel_time=900,
                    traffic_model=FastTrafficModel.PEAK,
                ),
            ],
            many_to_one=[],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 1


@pytest.mark.asyncio
async def test_many_to_one_with_traffic_model(async_client: AsyncClient):
    response = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[],
            many_to_one=[
                GeoHashFastSearch(
                    id="id",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=TransportationFast.DRIVING_FERRY,
                    travel_time=900,
                    traffic_model=FastTrafficModel.OFF_PEAK,
                ),
            ],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 1


def test_one_to_many_with_traffic_model_sync(client: Client):
    response = client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=TransportationFast.DRIVING,
                    travel_time=900,
                    traffic_model=FastTrafficModel.PEAK,
                ),
            ],
            many_to_one=[],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 1


def test_many_to_one_with_traffic_model_sync(client: Client):
    response = client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[],
            many_to_one=[
                GeoHashFastSearch(
                    id="id",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=TransportationFast.DRIVING_FERRY,
                    travel_time=900,
                    traffic_model=FastTrafficModel.OFF_PEAK,
                ),
            ],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 1
