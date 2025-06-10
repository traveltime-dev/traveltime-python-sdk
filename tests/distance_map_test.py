from datetime import datetime

import pytest

from traveltimepy import Driving
from traveltimepy.dto.common import Coordinates, LevelOfDetail
from traveltimepy.async_client import AsyncClient
from traveltimepy.dto.requests.distance_map import (
    DistanceMapDepartureSearch,
    DistanceMapArrivalSearch,
)


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient):
    results = await async_client.distance_map(
        arrival_searches=[],
        departure_searches=[
            DistanceMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
            ),
            DistanceMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
            ),
        ],
        unions=[],
        intersections=[],
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient):
    results = await async_client.distance_map(
        arrival_searches=[
            DistanceMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
            ),
            DistanceMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
            ),
        ],
        departure_searches=[],
        unions=[],
        intersections=[],
    )
    assert len(results) == 2
