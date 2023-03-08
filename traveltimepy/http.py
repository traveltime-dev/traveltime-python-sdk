import asyncio
from typing import Dict, Type, TypeVar

import aiohttp
from aiohttp import ClientResponse, ClientSession
from aiohttp_retry import RetryClient, ExponentialRetry
from pydantic.tools import parse_raw_as

from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.error import ResponseError
from traveltimepy.errors import ApiError
from traveltimepy.throttler import Throttler
from loguru import logger

T = TypeVar('T')
R = TypeVar('R')

DEFAULT_SPLIT_SIZE = 10


async def send_post_request_async(
    client: RetryClient,
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    window_size: int,
    throttler: Throttler
) -> T:
    url = f"https://api.traveltimeapp.com/v4/{path}"
    async with throttler.use(window_size):
        async with client.post(url=url, headers=headers, data=request.json()) as resp:
            return await __process_response(response_class, resp)


async def send_post_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    limit_per_host: int,
    retry_attempts: int,
    throttler: Throttler
) -> T:
    connector = aiohttp.TCPConnector(ssl=False, limit_per_host=limit_per_host)
    async with ClientSession(connector=connector) as session:
        client = RetryClient(client_session=session, retry_options=ExponentialRetry(attempts=retry_attempts))
        window_size = __window_size(throttler.rate_limit)
        parts = request.split_searches(window_size)
        logger.debug(f"Split {request.__class__.__name__} request into {len(parts)} parts.")
        tasks = [
            send_post_request_async(client, response_class, path, headers, part, window_size, throttler) for part in parts
        ]
        responses = await asyncio.gather(*tasks)
        return request.merge(responses)


def __window_size(rate_limit: int):
    if rate_limit >= DEFAULT_SPLIT_SIZE:
        return DEFAULT_SPLIT_SIZE
    else:
        return rate_limit


def send_post(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    limit_per_host: int,
    retry_attempts: int,
    throttler: Throttler
) -> T:
    return asyncio.run(send_post_async(response_class, path, headers, request, limit_per_host, retry_attempts, throttler))


async def send_get_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    params: Dict[str, str] = None
) -> T:
    connector = aiohttp.TCPConnector(ssl=False)
    url = f'https://api.traveltimeapp.com/v4/{path}'
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url=url, headers=headers, params=params) as resp:
            return await __process_response(response_class, resp)


def send_get(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    params: Dict[str, str] = None
) -> T:
    return asyncio.run(send_get_async(response_class, path, headers, params))


async def __process_response(response_class: Type[T], response: ClientResponse) -> T:
    text = await response.text()
    if response.status != 200:
        parsed = parse_raw_as(ResponseError, text)
        msg = 'Travel Time API request failed \n{}\nError code: {}\nAdditional info: {}\n<{}>\n'.format(
            parsed.description,
            parsed.error_code,
            parsed.additional_info,
            parsed.documentation_link
        )

        raise ApiError(msg)
    else:
        return parse_raw_as(response_class, text)
