import pytest
from unittest.mock import Mock, patch, AsyncMock
from tenacity import RetryError

from traveltimepy import Client, AsyncClient
from traveltimepy.errors import TravelTimeJsonError, TravelTimeServerError


class TestRetryLogic:
    def _mock_async_session(self):
        """Create async session mock to avoid HTTP requests."""
        mock_response = Mock()
        context_manager = Mock()
        context_manager.__aenter__ = AsyncMock(return_value=mock_response)
        context_manager.__aexit__ = AsyncMock(return_value=None)

        session = Mock()
        session.request.return_value = context_manager
        return session

    @pytest.mark.asyncio
    async def test_async_server_error_retries(self):
        async with AsyncClient("test", "test", retry_attempts=2) as client:
            with patch.object(
                client, "_get_session", return_value=self._mock_async_session()
            ):
                with patch.object(
                    client,
                    "_handle_response",
                    side_effect=TravelTimeServerError("Server error"),
                ) as mock_handle:
                    with pytest.raises(RetryError):
                        await client._make_request("GET", "https://test.com", {}, Mock)

                    assert mock_handle.call_count == 3  # initial + 2 retries

    def test_sync_server_error_retries(self):
        with Client("test", "test", retry_attempts=2) as client:
            with patch.object(client._session, "request", return_value=Mock()):
                with patch.object(
                    client,
                    "_handle_response",
                    side_effect=TravelTimeServerError("Server error"),
                ) as mock_handle:
                    with pytest.raises(RetryError):
                        client._make_request("GET", "https://test.com", {}, Mock)

                    assert mock_handle.call_count == 3  # initial + 2 retries

    @pytest.mark.asyncio
    async def test_async_client_error_no_retry(self):
        async with AsyncClient("test", "test", retry_attempts=3) as client:
            error = TravelTimeJsonError(400, "CLIENT_ERROR", "Bad request", "", {})

            with patch.object(
                client, "_make_request", side_effect=error
            ) as mock_request:
                with pytest.raises(TravelTimeJsonError):
                    await client._make_request("GET", "https://test.com", {}, Mock)

                assert mock_request.call_count == 1  # no retries for client errors

    def test_sync_client_error_no_retry(self):
        with Client("test", "test", retry_attempts=3) as client:
            error = TravelTimeJsonError(400, "CLIENT_ERROR", "Bad request", "", {})

            with patch.object(
                client, "_make_request", side_effect=error
            ) as mock_request:
                with pytest.raises(TravelTimeJsonError):
                    client._make_request("GET", "https://test.com", {}, Mock)

                assert mock_request.call_count == 1  # no retries for client errors

    @pytest.mark.asyncio
    async def test_async_server_error_no_retries_when_disabled(self):
        async with AsyncClient("test", "test", retry_attempts=0) as client:
            with patch.object(
                client, "_get_session", return_value=self._mock_async_session()
            ):
                with patch.object(
                    client,
                    "_handle_response",
                    side_effect=TravelTimeServerError("Server error"),
                ) as mock_handle:
                    with pytest.raises(RetryError):
                        await client._make_request("GET", "https://test.com", {}, Mock)

                    assert (
                        mock_handle.call_count == 1
                    )  # only initial attempt, no retries

    def test_sync_server_error_no_retries_when_disabled(self):
        with Client("test", "test", retry_attempts=0) as client:
            with patch.object(client._session, "request", return_value=Mock()):
                with patch.object(
                    client,
                    "_handle_response",
                    side_effect=TravelTimeServerError("Server error"),
                ) as mock_handle:
                    with pytest.raises(RetryError):
                        client._make_request("GET", "https://test.com", {}, Mock)

                    assert (
                        mock_handle.call_count == 1
                    )  # only initial attempt, no retries
