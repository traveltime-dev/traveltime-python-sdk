import pytest


@pytest.mark.asyncio
async def test_geocoding_search(sdk):
    response = await sdk.geocoding_async(
        query="Parliament square", limit=30, within_countries=["gb", "de"]
    )
    assert len(response.features) > 0
    assert len(response.features) < 31


@pytest.mark.asyncio
async def test_geocoding_reverse(sdk):
    response = await sdk.geocoding_reverse_async(lat=51.507281, lng=-0.132120)
    assert len(response.features) > 0
