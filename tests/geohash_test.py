from datetime import datetime

import pytest

from traveltimepy import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import (
    Coordinates,
    Range,
    GeohashCentroid,
    CellProperty,
)
from traveltimepy.requests.geohash import (
    GeoHashDepartureSearch,
    GeoHashArrivalSearch,
    GeoHashUnion,
    GeoHashIntersection,
)
from traveltimepy.requests.transportation import Driving, PublicTransport


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient):
    response = await async_client.geohash(
        arrival_searches=[],
        departure_searches=[
            GeoHashDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                transportation=Driving(),
                travel_time=900,
                departure_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
            GeoHashDepartureSearch(
                id="id 2",
                coords=GeohashCentroid(geohash_centroid="gcpvhb"),
                transportation=Driving(),
                travel_time=900,
                departure_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
        unions=[],
        intersections=[],
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient):
    response = await async_client.geohash(
        departure_searches=[],
        arrival_searches=[
            GeoHashArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                transportation=Driving(),
                travel_time=900,
                arrival_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
            GeoHashArrivalSearch(
                id="id 2",
                coords=GeohashCentroid(geohash_centroid="gcpvhb"),
                transportation=Driving(),
                travel_time=900,
                arrival_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
        unions=[],
        intersections=[],
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_union_departures(async_client: AsyncClient):
    response = await async_client.geohash(
        arrival_searches=[],
        departure_searches=[
            GeoHashDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                transportation=Driving(),
                travel_time=900,
                departure_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
            GeoHashDepartureSearch(
                id="id 2",
                coords=GeohashCentroid(geohash_centroid="gcpvhb"),
                transportation=PublicTransport(),
                travel_time=900,
                departure_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
        unions=[GeoHashUnion(id="union", search_ids=["id", "id 2"])],
        intersections=[],
    )

    assert len(response.results) == 3


@pytest.mark.asyncio
async def test_intersection_arrivals(async_client: AsyncClient):
    response = await async_client.geohash(
        departure_searches=[],
        arrival_searches=[
            GeoHashArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                transportation=Driving(),
                travel_time=900,
                arrival_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
            GeoHashArrivalSearch(
                id="id 2",
                coords=GeohashCentroid(geohash_centroid="gcpvhb"),
                transportation=Driving(),
                travel_time=900,
                arrival_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
        unions=[],
        intersections=[
            GeoHashIntersection(id="intersection", search_ids=["id", "id 2"])
        ],
    )

    assert len(response.results) == 3


def test_departures_sync(client: Client):
    response = client.geohash(
        arrival_searches=[],
        departure_searches=[
            GeoHashDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                transportation=Driving(),
                travel_time=900,
                departure_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
            GeoHashDepartureSearch(
                id="id 2",
                coords=GeohashCentroid(geohash_centroid="gcpvhb"),
                transportation=Driving(),
                travel_time=900,
                departure_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
        unions=[],
        intersections=[],
    )

    assert len(response.results) == 2


def test_arrivals_sync(client: Client):
    response = client.geohash(
        departure_searches=[],
        arrival_searches=[
            GeoHashArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                transportation=Driving(),
                travel_time=900,
                arrival_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
            GeoHashArrivalSearch(
                id="id 2",
                coords=GeohashCentroid(geohash_centroid="gcpvhb"),
                transportation=Driving(),
                travel_time=900,
                arrival_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
        unions=[],
        intersections=[],
    )

    assert len(response.results) == 2


def test_union_departures_sync(client: Client):
    response = client.geohash(
        arrival_searches=[],
        departure_searches=[
            GeoHashDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                transportation=Driving(),
                travel_time=900,
                departure_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
            GeoHashDepartureSearch(
                id="id 2",
                coords=GeohashCentroid(geohash_centroid="gcpvhb"),
                transportation=PublicTransport(),
                travel_time=900,
                departure_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
        unions=[GeoHashUnion(id="union", search_ids=["id", "id 2"])],
        intersections=[],
    )

    assert len(response.results) == 3


def test_intersection_arrivals_sync(client: Client):
    response = client.geohash(
        departure_searches=[],
        arrival_searches=[
            GeoHashArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                transportation=Driving(),
                travel_time=900,
                arrival_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
            GeoHashArrivalSearch(
                id="id 2",
                coords=GeohashCentroid(geohash_centroid="gcpvhb"),
                transportation=Driving(),
                travel_time=900,
                arrival_time=datetime.now(),
                range=Range(enabled=True, width=1800),
            ),
        ],
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
        unions=[],
        intersections=[
            GeoHashIntersection(id="intersection", search_ids=["id", "id 2"])
        ],
    )

    assert len(response.results) == 3
