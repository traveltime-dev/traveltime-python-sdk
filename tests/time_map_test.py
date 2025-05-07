import pytest
from datetime import datetime

from traveltimepy import Coordinates, Driving, LevelOfDetail, Range, TravelTimeSdk


@pytest.mark.asyncio
async def test_departures(sdk: TravelTimeSdk):
    results = await sdk.time_map_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_departures_geojson(sdk: TravelTimeSdk):
    results = await sdk.time_map_geojson_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(results.features) == 2


@pytest.mark.asyncio
async def test_departures_wkt(sdk: TravelTimeSdk):
    response = await sdk.time_map_wkt_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_departures_wkt_no_holes(sdk: TravelTimeSdk):
    response = await sdk.time_map_wkt_no_holes_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_arrivals(sdk: TravelTimeSdk):
    results = await sdk.time_map_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals_geojson(sdk: TravelTimeSdk):
    results = await sdk.time_map_geojson_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(results.features) == 2


@pytest.mark.asyncio
async def test_arrivals_wkt(sdk: TravelTimeSdk):
    response = await sdk.time_map_wkt_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_arrivals_wkt_no_holes(sdk: TravelTimeSdk):
    response = await sdk.time_map_wkt_no_holes_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_union_departures(sdk: TravelTimeSdk):
    result = await sdk.time_map_union_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(result.shapes) > 0


@pytest.mark.asyncio
async def test_intersection_arrivals(sdk: TravelTimeSdk):
    result = await sdk.time_map_intersection_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
        search_range=Range(enabled=True, width=1800),
        level_of_detail=LevelOfDetail(scale_type="simple", level="lowest"),
    )
    assert len(result.shapes) > 0
