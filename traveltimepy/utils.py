from typing import TypeVar, Type, Dict

import aiohttp
import requests
from pydantic.main import BaseModel
from pydantic.tools import parse_raw_as
from traveltimepy import AcceptType, TimeFilterFastResponse_pb2

from traveltimepy.dto.requests.time_filter_proto import TimeFilterProtoRequest
from traveltimepy.dto.responses.error import ResponseError
from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.errors import ApiError


T = TypeVar('T')
R = TypeVar('R')


async def send_post_request_async(response_class: Type[T], path: str, headers: Dict[str, str], body: BaseModel) -> T:
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=body.json()) as resp:
            body_text = await resp.text()
            return __process_response(response_class, resp.status, body_text)


async def send_get_request_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    params: Dict[str, str] = None
) -> T:
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, params=params) as resp:
            body_text = await resp.text()
            return __process_response(response_class, resp.status, body_text)


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


def send_get_request(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    params: Dict[str, str] = None
) -> T:
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
    resp = requests.get(url=url, headers=headers, params=params)
    return __process_response(response_class, resp.status_code, resp.text)


def send_post_request(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    body: BaseModel
) -> T:
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
    resp = requests.post(url=url, headers=headers, data=body.json())
    return __process_response(response_class, resp.status_code, resp.text)


def __process_response(response_class: Type[T], status_code: int, text: str) -> T:
    if status_code != 200:
        parsed = parse_raw_as(ResponseError, text)
        msg = 'Travel Time API request failed \n{}\nError code: {}\n<{}>\n'.format(
            parsed.description,
            parsed.error_code,
            parsed.documentation_link
        )

        raise ApiError(msg)

    return parse_raw_as(response_class, text)
