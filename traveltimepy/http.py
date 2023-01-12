import asyncio
from typing import TypeVar, Type, Dict

import aiohttp
import requests
from aiohttp import ClientSession, ClientResponse
from pydantic.tools import parse_raw_as
from traveltimepy import AcceptType, TimeFilterFastResponse_pb2
from traveltimepy.dto.requests.request import TravelTimeRequest

from traveltimepy.dto.requests.time_filter_proto import TimeFilterProtoRequest
from traveltimepy.dto.responses.error import ResponseError
from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
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
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
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
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
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


def send_proto_request(
    proto_request: TimeFilterProtoRequest,
    app_id: str,
    api_key: str
) -> TimeFilterProtoResponse:
    country = proto_request.one_to_many.country.value
    transport = proto_request.one_to_many.transportation.value.name
    url = '/'.join(['https://proto.api.traveltimeapp.com', 'api', 'v2', country, 'time-filter', 'fast', transport])

    resp = requests.post(
        url,
        headers={'Content-Type': AcceptType.OCTET_STREAM.value, 'User-Agent': 'Travel Time Python SDK'},
        data=proto_request.to_proto().SerializeToString(),
        auth=(app_id, api_key)
    )

    response_body = TimeFilterFastResponse_pb2.TimeFilterFastResponse()

    if resp.status_code != 200:
        msg = 'Travel Time API proto request failed with error code: {}\n'.format(resp.status_code)
        raise ApiError(msg)

    response_body.ParseFromString(resp.content)
    return TimeFilterProtoResponse(travel_times=response_body.properties.travelTimes[:])


async def __process_response(response_class: Type[T], response: ClientResponse) -> T:
    text = await response.text()
    if response.status != 200:
        parsed = parse_raw_as(ResponseError, text)
        msg = 'Travel Time API request failed \n{}\nError code: {}\nMsg: {}\n<{}>\n'.format(
            parsed.description,
            parsed.error_code,
            parsed.additional_info,
            parsed.documentation_link
        )

        raise ApiError(msg)
    else:
        return parse_raw_as(response_class, text)
