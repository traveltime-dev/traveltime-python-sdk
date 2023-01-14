import asyncio
from typing import TypeVar, Type, Dict

import aiohttp
from aiohttp import ClientSession, ClientResponse
from pydantic.tools import parse_raw_as
from traveltimepy.dto.requests.request import TravelTimeRequest

from traveltimepy.dto.responses.error import ResponseError
from traveltimepy.errors import ApiError

T = TypeVar('T')
R = TypeVar('R')


async def send_post_request_async(
    session: ClientSession,
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest
) -> T:
    url = f'https://api.traveltimeapp.com/v4/{path}'
    async with session.post(url=url, headers=headers, data=request.json()) as resp:
        return await __process_response(response_class, resp)


async def __gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem(task) for task in tasks))


async def send_post_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest
) -> T:
    async with ClientSession() as session:
        tasks = [send_post_request_async(session, response_class, path, headers, part) for part in request.split_searches()]
        responses = await __gather_with_concurrency(5, *tasks)
        return request.merge(responses)


def send_post(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    request: TravelTimeRequest
) -> T:
    return asyncio.run(send_post_async(response_class, path, headers, request))


async def send_get_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    params: Dict[str, str] = None
) -> T:
    url = f'https://api.traveltimeapp.com/v4/{path}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, params=params) as resp:
            return await __process_response(response_class, resp)


def send_get(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    params: Dict[str, str] = None
) -> T:
    print(params)
    return asyncio.run(send_get_async(response_class, path, headers, params))


async def __process_response(response_class: Type[T], response: ClientResponse) -> T:
    text = await response.text()
    if response.status != 200:
        print(text)

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
