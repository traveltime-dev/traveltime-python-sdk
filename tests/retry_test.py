import asyncio

import aiohttp
import pytest
import requests
from unittest.mock import Mock, patch, AsyncMock
from tenacity import RetryError

from traveltimepy import Client, AsyncClient, base_client
from traveltimepy.errors import TravelTimeJsonError, TravelTimeServerError

RATE_LIMITED = TravelTimeJsonError(429, "9", "Too many requests", "", {})


@pytest.fixture(autouse=True)
def no_retry_delays(monkeypatch):
    monkeypatch.setattr(base_client, "SERVER_RETRY_BASE_DELAY", 0)
    monkeypatch.setattr(base_client, "SERVER_RETRY_JITTER", 0)
    monkeypatch.setattr(base_client, "RATE_LIMIT_RETRY_DELAY", 0)
    monkeypatch.setattr(base_client, "RATE_LIMIT_RETRY_JITTER", 0)


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

    @pytest.mark.asyncio
    async def test_async_rate_limit_retries(self):
        async with AsyncClient("test", "test", rate_limit_retry_attempts=2) as client:
            with patch.object(
                client, "_get_session", return_value=self._mock_async_session()
            ):
                with patch.object(
                    client, "_handle_response", side_effect=RATE_LIMITED
                ) as mock_handle:
                    with pytest.raises(TravelTimeJsonError):
                        await client._make_request("GET", "https://test.com", {}, Mock)

                    assert mock_handle.call_count == 3  # initial + 2 retries

    def test_sync_rate_limit_retries(self):
        with Client("test", "test", rate_limit_retry_attempts=2) as client:
            with patch.object(client._session, "request", return_value=Mock()):
                with patch.object(
                    client, "_handle_response", side_effect=RATE_LIMITED
                ) as mock_handle:
                    with pytest.raises(TravelTimeJsonError):
                        client._make_request("GET", "https://test.com", {}, Mock)

                    assert mock_handle.call_count == 3  # initial + 2 retries

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "error, raised, calls",
        [
            (aiohttp.ServerDisconnectedError(), aiohttp.ServerDisconnectedError, 3),
            (asyncio.TimeoutError(), asyncio.TimeoutError, 1),
        ],
    )
    async def test_async_connection_errors(self, error, raised, calls):
        async with AsyncClient("test", "test", retry_attempts=2) as client:
            session = self._mock_async_session()
            session.request.side_effect = error
            with patch.object(client, "_get_session", return_value=session):
                with pytest.raises(raised):
                    await client._make_request("GET", "https://test.com", {}, Mock)

                assert session.request.call_count == calls

    @pytest.mark.parametrize(
        "error, raised, calls",
        [
            (
                requests.exceptions.ConnectionError(),
                requests.exceptions.ConnectionError,
                3,
            ),
            (requests.exceptions.ReadTimeout(), requests.exceptions.ReadTimeout, 1),
        ],
    )
    def test_sync_connection_errors(self, error, raised, calls):
        with Client("test", "test", retry_attempts=2) as client:
            with patch.object(
                client._session, "request", side_effect=error
            ) as mock_request:
                with pytest.raises(raised):
                    client._make_request("GET", "https://test.com", {}, Mock)

                assert mock_request.call_count == calls
