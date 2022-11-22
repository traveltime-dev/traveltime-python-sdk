import dataclasses
import json

from dacite import from_dict
from datetime import datetime
from typing import TypeVar, Type, Dict, Optional

import aiohttp
import requests

from traveltime.dto.responses.error import ResponseError
from traveltime.errors import ApiError


T = TypeVar('T')
R = TypeVar('R')


async def send_post_request_async(response_class: Type[T], path: str, headers: Dict[str, str], body: R) -> T:
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=to_json(body)) as resp:
            json_body = resp.json()
            process_error(resp.status_code, json_body)
            return from_json(response_class, json_body)


async def send_get_request_async(
    response_class: Type[T],
    path: str,
    headers: Dict[str, str],
    query: Optional[str] = None
) -> T:
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, query=query) as resp:
            json_body = resp.json()
            process_error(resp.status_code, json_body)
            return from_json(response_class, json_body)


def send_get_request(response_class: Type[T], path: str, headers: Dict[str, str], query: Optional[str] = None) -> T:
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
    resp = requests.get(url=url, headers=headers, params=query)
    json_body = resp.json()
    process_error(resp.status_code, json_body)
    return from_json(response_class, json_body)


def send_post_request(response_class: Type[T], path: str, headers: Dict[str, str], body: R) -> T:
    url = '/'.join(['https://api.traveltimeapp.com', 'v4', path])
    resp = requests.post(url=url, headers=headers, data=to_json(body))
    json_body = resp.json()
    process_error(resp.status_code, json_body)
    return from_json(response_class, json_body)


def process_error(status_code: int, json_body: str):
    if status_code != 200:
        parsed = from_json(ResponseError, json_body)
        msg = 'Travel Time API request failed \n{}\nError code: {}\n<{}>\n'.format(
            parsed.description,
            parsed.error_code,
            parsed.documentation_link
        )

        raise ApiError(msg)


def object_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.fromisoformat(value)
        except:
            json_dict[key] = value

    return json_dict


def from_json(data_class: Type[T], value: str) -> T:
    return from_dict(data_class=data_class, data=json.loads(value, object_hook=object_hook))


def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()


def to_json(value: T) -> str:
    return json.dumps(dataclasses.asdict(value), default=default)
