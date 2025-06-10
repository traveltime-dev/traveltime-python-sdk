import pytest
from datetime import datetime

from traveltimepy import Coordinates, Driving, LevelOfDetail, Range
from traveltimepy.async_client import AsyncClient
from traveltimepy.dto.requests.time_map import TimeMapDepartureSearch, TimeMapArrivalSearch, TimeMapUnion, \
    TimeMapIntersection


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient):
    results = await async_client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ],
        unions=[],
        intersections=[]
    )
    assert len(results) == 2

@pytest.mark.asyncio
async def test_departures_geojson(async_client: AsyncClient):
    results = await async_client.time_map_geojson(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ]
    )
    assert len(results.features) == 2

@pytest.mark.asyncio
async def test_departures_wkt(async_client: AsyncClient):
    results = await async_client.time_map_wkt(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ]
    )
    assert len(results.results) == 2

@pytest.mark.asyncio
async def test_departures_wkt_no_holes(async_client: AsyncClient):
    results = await async_client.time_map_wkt_no_holes(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ]
    )
    assert len(results.results) == 2


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient):
    results = await async_client.time_map(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ],
        unions=[],
        intersections=[]
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals_geojson(async_client: AsyncClient):
    results = await async_client.time_map_geojson(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ]
    )
    assert len(results.features) == 2


@pytest.mark.asyncio
async def test_arrivals_wkt(async_client: AsyncClient):
    results = await async_client.time_map_wkt(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ]
    )
    assert len(results.results) == 2


@pytest.mark.asyncio
async def test_arrivals_wkt_no_holes(async_client: AsyncClient):
    results = await async_client.time_map_wkt_no_holes(
        departure_searches=[],
        arrival_searches=[
            TimeMapArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapArrivalSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                arrival_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ]
    )
    assert len(results.results) == 2


@pytest.mark.asyncio
async def test_union_departures(async_client: AsyncClient):
    results = await async_client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ],
        unions=[
            TimeMapUnion(
                id="union",
                search_ids=["id", "id 2"]
            )
        ],
        intersections=[]
    )
    assert len(results[0].shapes) > 0



@pytest.mark.asyncio
async def test_intersection_departures(async_client: AsyncClient):
    results = await async_client.time_map(
        arrival_searches=[],
        departure_searches=[
            TimeMapDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            ),
            TimeMapDepartureSearch(
                id="id 2",
                coords=Coordinates(lat=51.517609, lng=-0.138315),
                departure_time=datetime.now(),
                travel_time=900,
                transportation=Driving(),
                range=Range(enabled=True, width=1800),
                level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")
            )
        ],
        unions=[],
        intersections=[
            TimeMapIntersection(
                id="union",
                search_ids=["id", "id 2"]
            )
        ]
    )
    assert len(results[0].shapes) > 0
