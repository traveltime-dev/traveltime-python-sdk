import pytest

from traveltimepy.async_client import AsyncClient


@pytest.mark.asyncio
async def test_map_info(async_client: AsyncClient):
    maps = await async_client.map_info()
    assert len(maps) > 0
