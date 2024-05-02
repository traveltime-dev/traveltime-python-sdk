import pytest

from traveltimepy import Transportation, TravelTimeSdk


@pytest.mark.asyncio
async def test_one_to_many(sdk: TravelTimeSdk, locations):
    results = await sdk.time_filter_fast_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=Transportation(type="public_transport"),
    )

    assert len(results) > 0


@pytest.mark.asyncio
async def test_many_to_one(sdk: TravelTimeSdk, locations):
    results = await sdk.time_filter_fast_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=Transportation(type="public_transport"),
        one_to_many=False,
    )

    assert len(results) > 0
