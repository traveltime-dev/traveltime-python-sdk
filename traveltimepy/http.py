import asyncio
from dataclasses import dataclass
from typing import TypeVar, Type, Dict

from aiohttp import ClientSession, ClientResponse, TCPConnector
from pydantic.tools import parse_raw_as
from traveltimepy.dto.requests.request import TravelTimeRequest

from traveltimepy.dto.responses.error import ResponseError
from traveltimepy.errors import ApiError
from aiohttp_retry import RetryClient, ExponentialRetry
from aiolimiter import AsyncLimiter

T = TypeVar("T")
DEFAULT_SPLIT_SIZE = 10


@dataclass
class SdkParams:
    host: str
    proto_host: str
    limit_per_host: int
    rate_limit: int
    time_window: int
    retry_attempts: int


async def send_post_request_async(
    client: RetryClient,
    response_class: Type[T],
    url: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    rate_limit: AsyncLimiter,
) -> T:
    async with rate_limit:
        async with client.post(url=url, headers=headers, data=request.json()) as resp:
            return await _process_response(response_class, resp)


async def send_post_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    sdk_params: SdkParams,
) -> T:
    window_size = _window_size(sdk_params.rate_limit)
    async with ClientSession(
        connector=TCPConnector(ssl=False, limit_per_host=sdk_params.limit_per_host)
    ) as session:
        retry_options = ExponentialRetry(attempts=sdk_params.retry_attempts)
        async with RetryClient(
            client_session=session, retry_options=retry_options
        ) as client:
            rate_limit = AsyncLimiter(
                sdk_params.rate_limit // window_size, sdk_params.time_window
            )
            tasks = [
                send_post_request_async(
                    client,
                    response_class,
                    f"https://{sdk_params.host}/v4/{path}",
                    headers,
                    part,
                    rate_limit,
                )
                for part in request.split_searches(window_size)
            ]
            responses = await asyncio.gather(*tasks)
            return request.merge(responses)


async def send_post_geojson_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    sdk_params: SdkParams,
) -> T:
    window_size = _window_size(sdk_params.rate_limit)
    async with ClientSession(
        connector=TCPConnector(ssl=False, limit_per_host=sdk_params.limit_per_host)
    ) as session:
        retry_options = ExponentialRetry(attempts=sdk_params.retry_attempts)
        async with RetryClient(
            client_session=session, retry_options=retry_options
        ) as client:
            rate_limit = AsyncLimiter(
                sdk_params.rate_limit // window_size, sdk_params.time_window
            )
            tasks = [
                send_post_request_async(
                    client,
                    response_class,
                    f"https://{sdk_params.host}/v4/{path}",
                    headers,
                    request,
                    rate_limit,
                )
            ]
            responses = await asyncio.gather(*tasks)
            return request.merge(responses)


def _window_size(rate_limit: int):
    if rate_limit >= DEFAULT_SPLIT_SIZE:
        return DEFAULT_SPLIT_SIZE
    else:
        return rate_limit


async def send_get_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    sdk_params: SdkParams,
    params: Dict[str, str] = None,
) -> T:
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        retry_options = ExponentialRetry(attempts=sdk_params.retry_attempts)
        async with RetryClient(
            client_session=session, retry_options=retry_options
        ) as client:
            async with client.get(
                url=f"https://{sdk_params.host}/v4/{path}",
                headers=headers,
                params=params,
            ) as resp:
                return await _process_response(response_class, resp)


async def _process_response(response_class: Type[T], response: ClientResponse) -> T:
    text = await response.text()
    if response.status != 200:
        parsed = parse_raw_as(ResponseError, text)
        msg = (
            f"Travel Time API request failed: {parsed.description}\n"
            f"Error code: {parsed.error_code}\n"
            f"Additional info: {parsed.additional_info}\n"
            f"<{parsed.documentation_link}>\n"
        )
        raise ApiError(msg)
    else:
        return parse_raw_as(response_class, text)
