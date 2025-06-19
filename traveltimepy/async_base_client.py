import asyncio
import json
from typing import Optional, Dict, TypeVar, Type

import aiohttp
from aiohttp import ClientSession, ClientResponse, TCPConnector, BasicAuth
from aiohttp_retry import RetryClient, ExponentialRetry
from aiolimiter import AsyncLimiter
from pydantic import BaseModel

import TimeFilterFastResponse_pb2  # type: ignore
from traveltimepy.accept_type import AcceptType
from traveltimepy.base_client import BaseClient, __version__
from traveltimepy.errors import ApiError
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
        retry_attempts: Number of retry attempts for failed requests (default: 3)
        max_rpm: Maximum requests per minute for rate limiting (default: 60)
        session: Optional existing aiohttp ClientSession to use
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
        session: Optional[ClientSession] = None,
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
        self.session = session
        self.async_limiter = AsyncLimiter(max_rate=self.max_rpm, time_period=60)

    async def _get_session(self):
        use_running_session = self.session and not self.session.closed
        if use_running_session:
            return self.session
        else:
            return aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                connector=TCPConnector(ssl=self.use_ssl),
            )

    async def _make_request(
        self,
        client: RetryClient,
        method: str,
        url: str,
        headers: Dict[str, str],
        response_class: Type[T],
        data: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> T:
        async with self.async_limiter:
            async with client.request(
                method=method, url=url, headers=headers, data=data, params=params
            ) as response:
                return await self._handle_response(response, response_class)

    async def _api_call_post(
        self,
        response_class: Type[T],
        endpoint: str,
        accept_type: AcceptType,
        request: TravelTimeRequest,
    ) -> T:
        session = await self._get_session()
        url = self._build_url(endpoint)

        async with RetryClient(
            client_session=session,
            retry_options=ExponentialRetry(attempts=self.retry_attempts),
        ) as client:
            split_size = 10 if self.split_large_requests else 1

            tasks = [
                self._make_request(
                    client,
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
        session = await self._get_session()
        url = self._build_url(endpoint)

        async with RetryClient(
            client_session=session,
            retry_options=ExponentialRetry(attempts=self.retry_attempts),
        ) as client:
            return await self._make_request(
                client,
                "GET",
                url,
                self._get_json_headers(accept_type),
                response_class,
                params=params,
            )

    async def _api_call_proto(
        self, req: TimeFilterFastProtoRequest
    ) -> TimeFilterProtoResponse:
        session = await self._get_session()

        async with RetryClient(
            client_session=session,
            retry_options=ExponentialRetry(attempts=self.retry_attempts),
        ) as client:
            async with self.async_limiter:
                if isinstance(req.transportation, ProtoTransportation):
                    transportation_mode = req.transportation.value.name
                else:
                    transportation_mode = req.transportation.TYPE.value.name

                async with client.post(
                    url=f"https://{self._proto_host}/api/v2/{req.country.value}/time-filter/fast/{transportation_mode}",
                    headers=self._get_proto_headers(),
                    data=req.get_request().SerializeToString(),
                    auth=BasicAuth(self.app_id, self.api_key),
                ) as response:
                    content = await response.read()
                    if response.status != 200:
                        msg = self._build_proto_error_message(
                            response.status, response.headers
                        )

                        raise ApiError(msg)
                    else:
                        response_body = (
                            TimeFilterFastResponse_pb2.TimeFilterFastResponse()  # type: ignore
                        )
                        response_body.ParseFromString(content)
                        return TimeFilterProtoResponse(
                            travel_times=response_body.properties.travelTimes[:],
                            distances=response_body.properties.distances[:],
                        )

    async def _handle_response(
        self, response: ClientResponse, response_class: Type[T]
    ) -> T:
        text = await response.text()
        json_data = json.loads(text)
        if response.status != 200:
            parsed = ResponseError.model_validate_json(json.dumps(json_data))
            msg = self._build_api_error_message(parsed)
            raise ApiError(msg)
        else:
            return response_class.model_validate(json_data)
