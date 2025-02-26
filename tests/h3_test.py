import pytest
from datetime import datetime

from traveltimepy import Coordinates, Driving, Range, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, H3Centroid


@pytest.mark.asyncio
async def test_departures(sdk: TravelTimeSdk):
    results = await sdk.h3_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals(sdk: TravelTimeSdk):
    results = await sdk.h3_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_union_departures(sdk: TravelTimeSdk):
    result = await sdk.h3_union_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
    )
    assert len(result.cells) > 0


@pytest.mark.asyncio
async def test_intersection_arrivals(sdk: TravelTimeSdk):
    result = await sdk.h3_intersection_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
    )
    assert len(result.cells) > 0
