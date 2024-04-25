import pytest
from datetime import datetime

from traveltimepy import Coordinates, Driving, LevelOfDetail, TravelTimeSdk


@pytest.mark.asyncio
async def test_departures(sdk: TravelTimeSdk):
    results = await sdk.distance_map_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_distance=900,
        transportation=Driving(),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals(sdk: TravelTimeSdk):
    results = await sdk.distance_map_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_distance=900,
        transportation=Driving(),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(results) == 2
