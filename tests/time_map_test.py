import pytest
from datetime import datetime

from traveltimepy import Coordinates, Driving


@pytest.mark.asyncio
async def test_departures(sdk):
    results = await sdk.time_map_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_departures_geojson(sdk):
    results = await sdk.time_map_geojson_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals(sdk):
    results = await sdk.time_map_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals_geojson(sdk):
    results = await sdk.time_map_geojson_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_union_departures(sdk):
    result = await sdk.union_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    )
    assert len(result.shapes) > 0


@pytest.mark.asyncio
async def test_intersection_arrivals(sdk):
    result = await sdk.intersection_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    )
    assert len(result.shapes) > 0
