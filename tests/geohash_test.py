import pytest
from datetime import datetime

from traveltimepy import Coordinates, Driving, Range, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, GeohashCentroid


@pytest.mark.asyncio
async def test_departures(sdk: TravelTimeSdk):
    results = await sdk.geohash_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            GeohashCentroid(geohash_centroid="gcpvhb"),
        ],
        resolution=6,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals(sdk: TravelTimeSdk):
    results = await sdk.geohash_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            GeohashCentroid(geohash_centroid="gcpvhb"),
        ],
        resolution=6,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_union_departures(sdk: TravelTimeSdk):
    result = await sdk.geohash_union_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            GeohashCentroid(geohash_centroid="gcpvhb"),
        ],
        resolution=6,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
    )
    assert len(result.cells) > 0


@pytest.mark.asyncio
async def test_intersection_arrivals(sdk: TravelTimeSdk):
    result = await sdk.geohash_intersection_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            GeohashCentroid(geohash_centroid="gcpvhb"),
        ],
        resolution=6,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
    )
    assert len(result.cells) > 0
