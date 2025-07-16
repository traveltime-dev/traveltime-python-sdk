import asyncio
import json
from typing import Optional, Dict, TypeVar, Type

import aiohttp
from aiohttp import ClientSession, ClientResponse, BasicAuth, TCPConnector
from aiolimiter import AsyncLimiter
from pydantic import BaseModel
from tenacity import (
    retry,
    stop_after_attempt,
    wait_none,
    retry_if_exception_type,
)

import TimeFilterFastResponse_pb2  # type: ignore
from traveltimepy.accept_type import AcceptType
from traveltimepy.base_client import BaseClient, __version__
from traveltimepy.errors import (
    TravelTimeJsonError,
    TravelTimeProtoError,
    TravelTimeServerError,
)
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.requests.time_filter_proto import (
    TimeFilterFastProtoRequest,
    ProtoTransportation,
)
from traveltimepy.responses.error import ResponseError
from traveltimepy.responses.time_filter_proto import TimeFilterProtoResponse

T = TypeVar("T", bound=BaseModel)


class AsyncBaseClient(BaseClient):
    """
    Args:
        app_id: Your TravelTime API application ID
        api_key: Your TravelTime API key
        timeout: Request timeout in seconds (default: 300)
        retry_attempts: Number of retry attempts for 5xx server errors (default: 3)
        max_rpm: Maximum requests per minute for rate limiting (default: 60)
        use_ssl: Whether to use SSL for connections (default: True)
        split_large_requests: Split large requests into smaller requests for performance (default: True)
        _host: API host (default: "api.traveltimeapp.com")
        _proto_host: Proto API host (default: "proto.api.traveltimeapp.com")
        _user_agent: User agent string for requests
    """

    def __init__(
        self,
        app_id: str,
        api_key: str,
        timeout: int = 300,
        retry_attempts: int = 3,
        max_rpm: int = 60,
        use_ssl: bool = True,
        split_large_requests: bool = True,
        _host: str = "api.traveltimeapp.com",
        _proto_host: str = "proto.api.traveltimeapp.com",
        _user_agent: str = f"Travel Time Python SDK {__version__}",
    ):
        super().__init__(
            app_id=app_id,
            api_key=api_key,
            timeout=timeout,
            retry_attempts=retry_attempts,
            max_rpm=max_rpm,
            use_ssl=use_ssl,
            split_large_requests=split_large_requests,
            _host=_host,
            _proto_host=_proto_host,
            _user_agent=_user_agent,
        )
        self._session: Optional[ClientSession] = None
        self.async_limiter = AsyncLimiter(max_rate=self.max_rpm, time_period=60)

    async def close(self):
        """Close the aiohttp session if it exists."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _get_session(self) -> ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                connector=TCPConnector(ssl=self.use_ssl),
            )
        elif self._session.closed:
            raise RuntimeError("Session is closed")
        return self._session

    async def _make_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        response_class: Type[T],
        data: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> T:
        @retry(
            retry=retry_if_exception_type(TravelTimeServerError),
            stop=stop_after_attempt(
                self.retry_attempts + 1
            ),  # First attempt is not a retry, that's why `+1`
            wait=wait_none(),  # No wait between retries
        )
        async def _make_request_with_retry():
            session = await self._get_session()
            async with self.async_limiter:
                async with session.request(
                    method=method, url=url, headers=headers, data=data, params=params
                ) as response:
                    return await self._handle_response(response, response_class)

        return await _make_request_with_retry()

    async def _api_call_post(
        self,
        response_class: Type[T],
        endpoint: str,
        accept_type: AcceptType,
        request: TravelTimeRequest,
    ) -> T:
        url = self._build_url(endpoint)

        split_size = 10 if self.split_large_requests else 1

        tasks = [
            self._make_request(
                "POST",
                url,
                self._get_json_headers(accept_type),
                response_class,
                data=part.model_dump_json(),
            )
            for part in request.split_searches(split_size)
        ]
        responses = await asyncio.gather(*tasks)
        return request.merge(responses)

    async def _api_call_get(
        self,
        response_class: Type[T],
        endpoint: str,
        accept_type: AcceptType,
        params: Optional[Dict[str, str]],
    ) -> T:
        url = self._build_url(endpoint)

        return await self._make_request(
            "GET",
            url,
            self._get_json_headers(accept_type),
            response_class,
            params=params,
        )

    async def _api_call_proto(
        self, req: TimeFilterFastProtoRequest
    ) -> TimeFilterProtoResponse:
        @retry(
            retry=retry_if_exception_type(TravelTimeServerError),
            stop=stop_after_attempt(
                self.retry_attempts + 1
            ),  # First attempt is not a retry, that's why `+1`
            wait=wait_none(),  # No wait between retries
        )
        async def _make_proto_request():
            session = await self._get_session()
            async with self.async_limiter:
                if isinstance(req.transportation, ProtoTransportation):
                    transportation_mode = req.transportation.value.name
                else:
                    transportation_mode = req.transportation.TYPE.value.name

                async with session.post(
                    url=f"https://{self._proto_host}/api/v3/{req.country.value}/time-filter/fast/{transportation_mode}",
                    headers=self._get_proto_headers(),
                    data=req.get_request().SerializeToString(),
                    auth=BasicAuth(self.app_id, self.api_key),
                ) as response:
                    content = await response.read()
                    if response.status != 200:
                        if response.status >= 500:
                            raise TravelTimeServerError("Internal server error")
                        else:
                            raise TravelTimeProtoError(
                                status_code=response.status,
                                error_code=response.headers.get(
                                    "X-ERROR-CODE", "Unknown"
                                ),
                                error_details=response.headers.get(
                                    "X-ERROR-DETAILS", "No details provided"
                                ),
                                error_message=response.headers.get(
                                    "X-ERROR-MESSAGE", "No message provided"
                                ),
                            )
                    else:
                        response_body = (
                            TimeFilterFastResponse_pb2.TimeFilterFastResponse()  # type: ignore
                        )
                        response_body.ParseFromString(content)
                        return TimeFilterProtoResponse(
                            travel_times=response_body.properties.travelTimes[:],
                            distances=response_body.properties.distances[:],
                        )

        return await _make_proto_request()

    async def _handle_response(
        self, response: ClientResponse, response_class: Type[T]
    ) -> T:
        text = await response.text()
        json_data = json.loads(text)
        if response.status != 200:
            error = ResponseError.model_validate_json(json.dumps(json_data))
            if response.status >= 500:
                raise TravelTimeServerError(error.description)
            else:
                raise TravelTimeJsonError(
                    status_code=response.status,
                    error_code=str(error.error_code),
                    description=error.description,
                    documentation_link=error.documentation_link,
                    additional_info=error.additional_info,
                )
        else:
            return response_class.model_validate(json_data)
