import asyncio

from traveltimepy.dto.requests.time_filter_fast import Transportation


def test_one_to_many(sdk, locations):
    results = asyncio.run(sdk.time_filter_fast_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=Transportation(type="public_transport"),
    ))

    assert len(results) > 0


def test_many_to_one(sdk, locations):
    results = asyncio.run(sdk.time_filter_fast_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=Transportation(type="public_transport"),
        one_to_many=False,
    ))

    assert len(results) > 0
