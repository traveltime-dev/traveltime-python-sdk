import asyncio
import json
from typing import Optional, Dict, TypeVar, Type

import aiohttp
from aiohttp import ClientSession, ClientResponse, TCPConnector, BasicAuth
from aiohttp_retry import RetryClient, ExponentialRetry
from aiolimiter import AsyncLimiter
from pydantic import BaseModel

import TimeFilterFastResponse_pb2
from traveltimepy import ProtoTransportation, __version__
from traveltimepy.accept_type import AcceptType
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.requests.time_filter_proto import TimeFilterFastProtoRequest
from traveltimepy.dto.responses.error import ResponseError
from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.errors import ApiError

T = TypeVar("T", bound=BaseModel)


class AsyncBaseClient:
    def __init__(
        self,
        app_id: str,
        api_key: str,
        timeout: int = 300,
        retry_attempts: int = 3,
        max_rpm: int = 60,
        session: Optional[ClientSession] = None,
        use_ssl: bool = True,
        _host: str = "api.traveltimeapp.com",
        _proto_host: str = "proto.api.traveltimeapp.com",
        _user_agent: str = f"Travel Time Python SDK {__version__}",
        _split_size: int = 10,  # Splits requests to improve performance
    ):
        self.app_id = app_id
        self.api_key = api_key
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.max_rpm = max_rpm
        self.session = session
        self.use_ssl = use_ssl
        self._host = _host
        self._proto_host = _proto_host
        self._user_agent = _user_agent

        if _split_size <= max_rpm:
            self._split_size = _split_size
        else:
            self._split_size = max_rpm

        # TODO: Rework Async Limiter, right now it doesn't enforce limits correctly
        self.async_limiter = AsyncLimiter(self.max_rpm // self._split_size)

    def _build_url(self, endpoint: str) -> str:
        return f"https://{self._host}/v4/{endpoint}"

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
        response_class: Type[BaseModel],
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
            tasks = [
                self._make_request(
                    client,
                    "POST",
                    url,
                    self._get_json_headers(accept_type),
                    response_class,
                    data=part.model_dump_json(),
                )
                for part in request.split_searches(self._split_size)
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
                        error_code = response.headers.get("X-ERROR-CODE", "Unknown")
                        error_details = response.headers.get(
                            "X-ERROR-DETAILS", "No details provided"
                        )
                        error_message = response.headers.get(
                            "X-ERROR-MESSAGE", "No message provided"
                        )

                        msg = (
                            f"Travel Time API proto request failed with error code: {response.status}\n"
                            f"X-ERROR-CODE: {error_code}\n"
                            f"X-ERROR-DETAILS: {error_details}\n"
                            f"X-ERROR-MESSAGE: {error_message}"
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

    def _get_json_headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            "X-Application-Id": self.app_id,
            "X-Api-Key": self.api_key,
            "User-Agent": self._user_agent,
            "Content-Type": "application/json",
            "Accept": accept_type.value,
        }

    def _get_proto_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": AcceptType.OCTET_STREAM.value,
            "User-Agent": f"Travel Time Python SDK {__version__}",
        }

    async def _handle_response(
        self, response: ClientResponse, response_class: Type[T]
    ) -> T:
        text = await response.text()
        json_data = json.loads(text)
        if response.status != 200:
            parsed = ResponseError.model_validate_json(json.dumps(json_data))
            msg = (
                f"Travel Time API request failed: {parsed.description}\n"
                f"Error code: {parsed.error_code}\n"
                f"Additional info: {parsed.additional_info}\n"
                f"<{parsed.documentation_link}>\n"
            )
            raise ApiError(msg)
        else:
            return response_class.model_validate(json_data)
