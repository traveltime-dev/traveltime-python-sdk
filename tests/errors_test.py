from datetime import datetime
from unittest.mock import Mock, AsyncMock

import pytest

from traveltimepy import Client, AsyncClient
from traveltimepy.errors import TravelTimeApiError, TravelTimeError
from traveltimepy.requests.common import Coordinates
from traveltimepy.requests.time_map import TimeMapDepartureSearch
from traveltimepy.requests.transportation import Driving


@pytest.mark.asyncio
async def test_unauthorized():
    async with AsyncClient("invalid", "invalid") as client:
        with pytest.raises(TravelTimeApiError) as e:
            await client.map_info()
        assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_invalid_request(async_client: AsyncClient):
    with pytest.raises(TravelTimeApiError) as e:
        await async_client.time_map(
            arrival_searches=[],
            departure_searches=[
                TimeMapDepartureSearch(
                    id="id",
                    coords=Coordinates(
                        lat=39.77915419863149, lng=-71.97010300125959
                    ),  # North Atlantic Ocean
                    departure_time=datetime.now(),
                    travel_time=900,
                    transportation=Driving(),
                )
            ],
        )
    assert e.value.status_code == 422


def test_unauthorized_sync():
    invalid_client = Client("invalid", "invalid")
    with pytest.raises(TravelTimeApiError) as e:
        invalid_client.map_info()
    assert e.value.status_code == 401


def test_invalid_request_sync(client: Client):
    with pytest.raises(TravelTimeApiError) as e:
        client.time_map(
            arrival_searches=[],
            departure_searches=[
                TimeMapDepartureSearch(
                    id="id",
                    coords=Coordinates(
                        lat=39.77915419863149, lng=-71.97010300125959
                    ),  # North Atlantic Ocean
                    departure_time=datetime.now(),
                    travel_time=900,
                    transportation=Driving(),
                )
            ],
        )
    assert e.value.status_code == 422


def test_unexpected_error_response_sync():
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"unexpected": "format"}

    with Client("test", "test") as client:
        with pytest.raises(TravelTimeError, match="unexpected response"):
            client._handle_response(mock_response, Mock)


@pytest.mark.asyncio
async def test_unexpected_error_response_async():
    mock_response = AsyncMock()
    mock_response.status = 400
    mock_response.text.return_value = '{"unexpected": "format"}'

    async with AsyncClient("test", "test") as client:
        with pytest.raises(TravelTimeError, match="unexpected response"):
            await client._handle_response(mock_response, Mock)
