import pytest

from traveltimepy import AsyncClient


@pytest.mark.asyncio
async def test_geocoding_search(async_client: AsyncClient):
    response = await async_client.geocoding(
        query="Parliament square", limit=30, within_countries=["gb", "de"]
    )
    assert len(response.features) > 0
    assert len(response.features) < 31


@pytest.mark.asyncio
async def test_geocoding_reverse(async_client: AsyncClient):
    response = await async_client.reverse_geocoding(lat=51.507281, lng=-0.132120)
    assert len(response.features) > 0
