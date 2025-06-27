import pytest

from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client


@pytest.mark.asyncio
async def test_map_info(async_client: AsyncClient):
    maps = await async_client.map_info()
    assert len(maps) > 0


def test_map_info_sync(client: Client):
    maps = client.map_info()
    assert len(maps) > 0
