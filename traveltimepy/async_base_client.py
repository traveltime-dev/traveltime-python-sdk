import asyncio
import json
from typing import Optional, Dict, TypeVar, Type

import aiohttp
from aiohttp import ClientSession, ClientResponse
from aiohttp_retry import RetryClient, ExponentialRetry
from aiolimiter import AsyncLimiter
from pydantic import BaseModel

from traveltimepy.accept_type import AcceptType
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.error import ResponseError
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
        _host: str = "api.traveltimeapp.com",
        _proto_host: str = "proto.api.traveltimeapp.com",
        _user_agent: str = f"Travel Time Python SDK",
        _split_size: int = 10 # Splits requests to improve performance
    ):
        self.app_id = app_id
        self.api_key = api_key
        self._user_agent = _user_agent
        self.host = _host
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.max_rpm = max_rpm
        self.session = session

        if _split_size <= max_rpm:
            self._split_size = _split_size
        else:
            self._split_size = max_rpm

        self.async_limiter = AsyncLimiter(self.max_rpm // self._split_size)

    def _build_url(self, endpoint: str) -> str:
        return f"https://{self.host}/v4/{endpoint}"

    async def _get_session(self):
        use_running_session = self.session and not self.session.closed
        if use_running_session:
            return self.session
        else:
            return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))

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
                method=method,
                url=url,
                headers=headers,
                data=data,
                params=params
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
            client_session=session, retry_options=ExponentialRetry(attempts=self.retry_attempts)
        ) as client:
            tasks = [
                self._make_request(
                    client,
                    "POST",
                    url,
                    self._get_json_headers(accept_type),
                    response_class,
                    data=part.model_dump_json()
                )
                for part in request.split_searches(self._split_size)
            ]
            responses = await asyncio.gather(*tasks)
            return request.merge(responses)

    async def _api_call_get(
            self,
            response_class: Type[BaseModel],
            endpoint: str,
            accept_type: AcceptType,
            params: Optional[Dict[str, str]],
    ) -> T:
        session = await self._get_session()
        url = self._build_url(endpoint)

        async with RetryClient(
            client_session=session, retry_options=ExponentialRetry(attempts=self.retry_attempts)
        ) as client:
            return await self._make_request(
                client,
                "GET",
                url,
                self._get_json_headers(accept_type),
                response_class,
                params=params
            )

    def _get_json_headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            "X-Application-Id": self.app_id,
            "X-Api-Key": self.api_key,
            "User-Agent": self._user_agent,
            "Content-Type": "application/json",
            "Accept": accept_type.value,
        }

    async def _handle_response(self, response: ClientResponse, response_class: Type[T]) -> T:
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