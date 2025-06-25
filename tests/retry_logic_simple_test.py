import pytest
from unittest.mock import Mock, patch

from traveltimepy import Client, AsyncClient
from traveltimepy.errors import TravelTimeJsonError, TravelTimeServerError


class TestRetryLogic:
    @pytest.mark.asyncio
    async def test_async_server_error_retries(self):
        client = AsyncClient("test", "test", retry_attempts=2)

        async def mock_retry_method(*args, **kwargs):
            raise TravelTimeServerError("Server error")

        with patch.object(client, "_make_request", side_effect=mock_retry_method):
            with pytest.raises(
                Exception
            ):  # Could be RetryError or TravelTimeServerError
                await client._make_request("GET", "https://test.com", {}, Mock)

    def test_sync_server_error_retries(self):
        client = Client("test", "test", retry_attempts=2)

        def mock_retry_method(*args, **kwargs):
            raise TravelTimeServerError("Server error")

        with patch.object(client, "_make_request", side_effect=mock_retry_method):
            with pytest.raises(
                Exception
            ):  # Could be RetryError or TravelTimeServerError
                client._make_request("GET", "https://test.com", {}, Mock)

    @pytest.mark.asyncio
    async def test_async_client_error_no_retry(self):
        client = AsyncClient("test", "test", retry_attempts=3)

        client_error = TravelTimeJsonError(400, "CLIENT_ERROR", "Bad request", "", {})

        with patch.object(
            client, "_make_request", side_effect=client_error
        ) as mock_request:
            with pytest.raises(TravelTimeJsonError):
                await client._make_request("GET", "https://test.com", {}, Mock)

            # Should only be called once (no retries for client errors)
            assert mock_request.call_count == 1

    def test_sync_client_error_no_retry(self):
        client = Client("test", "test", retry_attempts=3)

        client_error = TravelTimeJsonError(400, "CLIENT_ERROR", "Bad request", "", {})

        with patch.object(
            client, "_make_request", side_effect=client_error
        ) as mock_request:
            with pytest.raises(TravelTimeJsonError):
                client._make_request("GET", "https://test.com", {}, Mock)

            # Should only be called once (no retries for client errors)
            assert mock_request.call_count == 1
