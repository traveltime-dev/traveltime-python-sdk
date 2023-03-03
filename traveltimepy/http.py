import asyncio
from typing import Dict, Optional, Type, TypeVar

import aiohttp
from aiohttp import ClientResponse, ClientSession
from aiohttp_retry import ExponentialRetry, RetryClient
from pydantic.tools import parse_raw_as

from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.error import ResponseError
from traveltimepy.errors import ApiError
from traveltimepy.utils.throttler import Throttler
from traveltimepy.utils.utils import count_api_hits

T = TypeVar('T')
R = TypeVar('R')

try:
    from loguru import logger
except ImportError:
    import logging

    logger = logging.getLogger(__name__)


# new function to send a POST request asynchronously to avoid
# duplicating this code inside the send_post_request_async function
async def _execute_post_request_async(
    client: RetryClient,
    response_class: Type[T],
    path: str,
    headers: dict[str, str],
    request: TravelTimeRequest,
) -> T:
    # Construct the URL for the API endpoint
    url = f"https://api.traveltimeapp.com/v4/{path}"
    # Send a POST request to the API with the given headers and data
    print(request.json())
    try:
        async with client.post(url=url, headers=headers, data=request.json()) as resp:
            # Process the response and return it as an instance of the given response class
            return await __process_response(response_class, resp)
    except Exception as e:
        logger.error(f"Error sending POST request to {url}: {e}")
        raise e


# update the send_post_request_async function to support use of a Throttler
async def send_post_request_async(
    client: RetryClient,
    response_class: Type[T],
    path: str,
    headers: dict[str, str],
    request: TravelTimeRequest,
    throttler: Optional[Throttler] = None,
) -> T:
    # If no throttler is provided, just send the POST request without throttling
    if throttler is None:
        return await _execute_post_request_async(client, response_class, path, headers, request)
    else:
        # Otherwise, use the throttler to enforce the request rate limit before sending the POST request
        async with throttler.use(count_api_hits(request)):
            return await _execute_post_request_async(
                client, response_class, path, headers, request
            )


# update the send_post_async function to support use of a Throttler
async def send_post_async(
    response_class: Type[T],
    path: str,
    headers: dict[str, str],
    request: TravelTimeRequest,
    limit_per_host: int,
    throttler: Optional[Throttler] = None,
) -> T:
    connector = aiohttp.TCPConnector(verify_ssl=False, limit_per_host=limit_per_host)
    async with ClientSession(
        connector=connector, timeout=aiohttp.ClientTimeout(total=60 * 60 * 30)
    ) as session:
        client = RetryClient(
            client_session=session, retry_options=ExponentialRetry(attempts=3), logger=logger
        )
        parts = request.split_searches()
        logger.debug(f"Split {request.__class__.__name__} request into {len(parts)} parts.")
        tasks = [
            send_post_request_async(client, response_class, path, headers, part, throttler)
            for part in parts
        ]
        responses = await asyncio.gather(*tasks)
        await client.close()
        return request.merge(responses)


# update the send_post function to support use of a Throttler
def send_post(
    response_class: Type[T],
    path: str,
    headers: dict[str, str],
    request: TravelTimeRequest,
    limit_per_host: int,
    throttler: Optional[Throttler] = None,
) -> T:
    return asyncio.run(
        send_post_async(response_class, path, headers, request, limit_per_host, throttler)
    )


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
