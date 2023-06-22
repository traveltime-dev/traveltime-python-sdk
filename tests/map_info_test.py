import asyncio


def test_map_info(sdk):
    maps = asyncio.run(sdk.map_info_async())
    assert len(maps) > 0
