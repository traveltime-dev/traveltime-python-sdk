import pytest

from traveltimepy import Transportation, TravelTimeSdk
from traveltimepy.dto.common import Coordinates


@pytest.mark.asyncio
async def test_one_to_many(sdk: TravelTimeSdk):
    results = await sdk.time_map_fast_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
    )

    assert len(results) == 2


@pytest.mark.asyncio
async def test_many_to_one(sdk: TravelTimeSdk):
    results = await sdk.time_map_fast_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
        one_to_many=False,
    )

    assert len(results) == 2


@pytest.mark.asyncio
async def test_one_to_many_geojson(sdk: TravelTimeSdk):
    results = await sdk.time_map_fast_geojson_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
    )

    assert len(results.features) == 2


@pytest.mark.asyncio
async def test_many_to_one_geojson(sdk: TravelTimeSdk):
    results = await sdk.time_map_fast_geojson_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
        one_to_many=False,
    )

    assert len(results.features) == 2


@pytest.mark.asyncio
async def test_one_to_many_wkt(sdk: TravelTimeSdk):
    response = await sdk.time_map_fast_wkt_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_many_to_one_wkt(sdk: TravelTimeSdk):
    response = await sdk.time_map_fast_wkt_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
        one_to_many=False,
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_one_to_many_wkt_no_holes(sdk: TravelTimeSdk):
    response = await sdk.time_map_fast_wkt_no_holes_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_many_to_one_wkt_no_holes(sdk: TravelTimeSdk):
    response = await sdk.time_map_fast_wkt_no_holes_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
        one_to_many=False,
    )

    assert len(response.results) == 2
