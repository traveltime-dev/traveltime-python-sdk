import asyncio
from dataclasses import dataclass
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


@dataclass
class SdkParams:
    host: str
    limit_per_host: int


async def send_post_request_async(
    client: RetryClient,
    response_class: Type[T],
    url: str,
    headers: Dict[str, str],
    request: TravelTimeRequest
) -> T:
    async with client.post(url=url, headers=headers, data=request.json()) as resp:
        return await __process_response(response_class, resp)


async def send_post_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    sdk_params: SdkParams
) -> T:
    connector = aiohttp.TCPConnector(ssl=False, limit_per_host=sdk_params.limit_per_host)
    async with ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60 * 60 * 30)) as session:
        client = RetryClient(client_session=session, retry_options=ExponentialRetry(attempts=3))
        tasks = [
            send_post_request_async(client, response_class, f'https://{sdk_params.host}/v4/{path}', headers, part)
            for part in request.split_searches()
        ]
        responses = await asyncio.gather(*tasks)
        await client.close()
        return request.merge(responses)


def send_post(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest,
    sdk_params: SdkParams
) -> T:
    return asyncio.run(send_post_async(response_class, path, headers, request, sdk_params))


async def send_get_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    sdk_params: SdkParams,
    params: Dict[str, str] = None
) -> T:
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url=f'https://{sdk_params.host}/v4/{path}', headers=headers, params=params) as resp:
            return await __process_response(response_class, resp)


def send_get(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    sdk_params: SdkParams,
    params: Dict[str, str] = None
) -> T:
    return asyncio.run(send_get_async(response_class, path, headers, sdk_params, params))


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
