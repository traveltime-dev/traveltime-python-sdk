import pytest

from traveltimepy import Transportation, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, Coordinates, H3Centroid


@pytest.mark.asyncio
async def test_one_to_many(sdk: TravelTimeSdk):
    results = await sdk.h3_fast_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
    )

    assert len(results) == 2


@pytest.mark.asyncio
async def test_many_to_one(sdk: TravelTimeSdk):
    results = await sdk.h3_fast_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        resolution=7,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        travel_time=900,
        transportation=Transportation(type="public_transport"),
        one_to_many=False,
    )

    assert len(results) == 2
