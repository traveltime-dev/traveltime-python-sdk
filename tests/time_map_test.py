import pytest
from datetime import datetime

from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Coordinates, Range
from traveltimepy.requests.level_of_detail import (
    SimpleLevelOfDetail,
    SimpleNumericLevelOfDetail,
    CoarseGridLevelOfDetail,
    Level,
    LevelOfDetail,
)
from traveltimepy.requests.time_map import (
    TimeMapDepartureSearch,
    TimeMapArrivalSearch,
    TimeMapUnion,
    TimeMapIntersection,
)
from traveltimepy.requests.transportation import Driving


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient):
    response = await async_client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
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
async def test_departures_geojson(async_client: AsyncClient):
    response = await async_client.time_map_geojson(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.features) == 2


@pytest.mark.asyncio
async def test_departures_wkt(async_client: AsyncClient):
    response = await async_client.time_map_wkt(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_departures_wkt_no_holes(async_client: AsyncClient):
    response = await async_client.time_map_wkt_no_holes(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient):
    response = await async_client.time_map(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
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
async def test_arrivals_geojson(async_client: AsyncClient):
    response = await async_client.time_map_geojson(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.features) == 2


@pytest.mark.asyncio
async def test_arrivals_wkt(async_client: AsyncClient):
    response = await async_client.time_map_wkt(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_arrivals_wkt_no_holes(async_client: AsyncClient):
    response = await async_client.time_map_wkt_no_holes(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_union_departures(async_client: AsyncClient):
    response = await async_client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        unions=[TimeMapUnion(id="union", search_ids=["id", "id 2"])],
        intersections=[],
    )
    assert len(response.results[0].shapes) > 0


@pytest.mark.asyncio
async def test_intersection_departures(async_client: AsyncClient):
    response = await async_client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        unions=[],
        intersections=[
            TimeMapIntersection(id="intersection", search_ids=["id", "id 2"])
        ],
    )
    assert len(response.results[0].shapes) > 0


@pytest.mark.asyncio
async def test_departures_simple_numeric_level_of_detail(async_client: AsyncClient):
    response = await async_client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleNumericLevelOfDetail(level=-5)
                ),
            ),
        ],
        unions=[],
        intersections=[],
    )
    assert len(response.results) == 1


@pytest.mark.asyncio
async def test_departures_coarse_grid_level_of_detail(async_client: AsyncClient):
    response = await async_client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=CoarseGridLevelOfDetail(square_size=1000)
                ),
            ),
        ],
        unions=[],
        intersections=[],
    )
    assert len(response.results) == 1


def test_departures_sync(client: Client):
    response = client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        unions=[],
        intersections=[],
    )
    assert len(response.results) == 2


def test_departures_geojson_sync(client: Client):
    response = client.time_map_geojson(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.features) == 2


def test_departures_wkt_sync(client: Client):
    response = client.time_map_wkt(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.results) == 2


def test_departures_wkt_no_holes_sync(client: Client):
    response = client.time_map_wkt_no_holes(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.results) == 2


def test_arrivals_sync(client: Client):
    response = client.time_map(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        unions=[],
        intersections=[],
    )
    assert len(response.results) == 2


def test_arrivals_geojson_sync(client: Client):
    response = client.time_map_geojson(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.features) == 2


def test_arrivals_wkt_sync(client: Client):
    response = client.time_map_wkt(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.results) == 2


def test_arrivals_wkt_no_holes_sync(client: Client):
    response = client.time_map_wkt_no_holes(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
    )
    assert len(response.results) == 2


def test_union_departures_sync(client: Client):
    response = client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        unions=[TimeMapUnion(id="union", search_ids=["id", "id 2"])],
        intersections=[],
    )
    assert len(response.results[0].shapes) > 0


def test_intersection_departures_sync(client: Client):
    response = client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(
                    scale_type=SimpleLevelOfDetail(level=Level.LOWEST)
                ),
            ),
        ],
        unions=[],
        intersections=[
            TimeMapIntersection(id="intersection", search_ids=["id", "id 2"])
        ],
    )
    assert len(response.results[0].shapes) > 0
