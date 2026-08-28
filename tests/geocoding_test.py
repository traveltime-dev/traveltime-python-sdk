import pytest

from traveltimepy import AsyncClient
from traveltimepy.client import Client


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


def test_geocoding_search_sync(client: Client):
    response = client.geocoding(
        query="Parliament square", limit=30, within_countries=["gb", "de"]
    )
    assert len(response.features) > 0
    assert len(response.features) < 31


def test_geocoding_reverse_sync(client: Client):
    response = client.reverse_geocoding(lat=51.507281, lng=-0.132120)
    assert len(response.features) > 0


@pytest.mark.asyncio
async def test_geocoding_search_with_language(async_client: AsyncClient):
    response = await async_client.geocoding(
        query="Parliament square", within_countries=["gb"], accept_language="de"
    )
    assert len(response.features) > 0


@pytest.mark.asyncio
async def test_geocoding_reverse_with_language(async_client: AsyncClient):
    response = await async_client.reverse_geocoding(
        lat=51.507281, lng=-0.132120, accept_language="de"
    )
    assert len(response.features) > 0


def test_geocoding_search_with_language_sync(client: Client):
    response = client.geocoding(
        query="Parliament square", within_countries=["gb"], accept_language="de"
    )
    assert len(response.features) > 0


def test_geocoding_reverse_with_language_sync(client: Client):
    response = client.reverse_geocoding(
        lat=51.507281, lng=-0.132120, accept_language="de"
    )
    assert len(response.features) > 0
