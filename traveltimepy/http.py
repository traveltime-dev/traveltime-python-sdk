import asyncio
from typing import TypeVar, Type, Dict

import aiohttp
from aiohttp import ClientSession, ClientResponse
from pydantic.tools import parse_raw_as
from traveltimepy.dto.requests.request import TravelTimeRequest

from traveltimepy.dto.responses.error import ResponseError
from traveltimepy.errors import ApiError
from aiohttp_retry import RetryClient, ExponentialRetry

T = TypeVar('T')
R = TypeVar('R')


async def send_post_request_async(
    client: RetryClient,
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest
) -> T:
    url = f'https://api.traveltimeapp.com/v4/{path}'
    async with client.post(url=url, headers=headers, data=request.json()) as resp:
        return await __process_response(response_class, resp)


async def send_post_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    limit_per_host: int
) -> T:
    connector = aiohttp.TCPConnector(verify_ssl=False, limit_per_host=limit_per_host)
    async with ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60 * 60 * 30)) as session:
        client = RetryClient(client_session=session, retry_options=ExponentialRetry(attempts=3))
        tasks = [send_post_request_async(client, response_class, path, headers, part) for part in request.split_searches()]
        responses = await asyncio.gather(*tasks)
        await client.close()
        return request.merge(responses)


def send_post(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    limit_per_host: int
) -> T:
    return asyncio.run(send_post_async(response_class, path, headers, request, limit_per_host))


async def send_get_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    params: Dict[str, str] = None
) -> T:
    connector = aiohttp.TCPConnector(verify_ssl=False)
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
