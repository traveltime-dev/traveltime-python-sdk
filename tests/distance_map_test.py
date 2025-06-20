from datetime import datetime

import pytest

from traveltimepy import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Coordinates
from traveltimepy.requests.distance_map import (
    DistanceMapDepartureSearch,
    DistanceMapArrivalSearch,
)
from traveltimepy.requests.level_of_detail import (
    LevelOfDetail,
    SimpleLevelOfDetail,
    Level,
)
from traveltimepy.requests.transportation import Driving


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient):
    response = await async_client.distance_map(
        arrival_searches=[],
        departure_searches=[
            DistanceMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            DistanceMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        unions=[],
        intersections=[],
    )
    assert len(response.results) == 2


def test_departures_sync(client: Client):
    response = client.distance_map(
        arrival_searches=[],
        departure_searches=[
            DistanceMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            DistanceMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        unions=[],
        intersections=[],
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient):
    response = await async_client.distance_map(
        arrival_searches=[
            DistanceMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            DistanceMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        departure_searches=[],
        unions=[],
        intersections=[],
    )
    assert len(response.results) == 2


def test_arrivals_sync(client: Client):
    response = client.distance_map(
        arrival_searches=[
            DistanceMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            DistanceMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_distance=900,
                transportation=Driving(),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        departure_searches=[],
        unions=[],
        intersections=[],
    )
    assert len(response.results) == 2
