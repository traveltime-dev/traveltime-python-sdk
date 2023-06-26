import pytest


@pytest.mark.asyncio
def test_map_info(sdk):
    maps = await sdk.map_info_async()
    assert len(maps) > 0
