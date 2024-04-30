import pytest

from traveltimepy.sdk import TravelTimeSdk


@pytest.mark.asyncio
async def test_map_info(sdk: TravelTimeSdk):
    maps = await sdk.map_info_async()
    assert len(maps) > 0
