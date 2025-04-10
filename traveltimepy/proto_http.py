from typing import Dict

from aiohttp import (
    ClientSession,
    ClientResponse,
    BasicAuth,
    TCPConnector,
    ClientTimeout,
)

import TimeFilterFastResponse_pb2  # type: ignore
import TimeFilterFastRequest_pb2  # type: ignore
from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.errors import ApiError


async def send_proto_async(
    url: str,
    headers: Dict[str, str],
    data: TimeFilterFastRequest_pb2.TimeFilterFastRequest,  # type: ignore
    app_id: str,
    api_key: str,
    timeout: int,
) -> TimeFilterProtoResponse:
    async with ClientSession(
        timeout=ClientTimeout(total=timeout), connector=TCPConnector(ssl=False)
    ) as session:
        async with session.post(
            url=url,
            headers=headers,
            data=data.SerializeToString(),
            auth=BasicAuth(app_id, api_key),
        ) as resp:
            return await _process_response(resp)


async def _process_response(response: ClientResponse) -> TimeFilterProtoResponse:
    content = await response.read()
    if response.status != 200:
        error_code = response.headers.get("X-ERROR-CODE", "Unknown")
        error_details = response.headers.get("X-ERROR-DETAILS", "No details provided")
        error_message = response.headers.get("X-ERROR-MESSAGE", "No message provided")

        msg = (
            f"Travel Time API proto request failed with error code: {response.status}\n"
            f"X-ERROR-CODE: {error_code}\n"
            f"X-ERROR-DETAILS: {error_details}\n"
            f"X-ERROR-MESSAGE: {error_message}"
        )

        raise ApiError(msg)
    else:
        response_body = TimeFilterFastResponse_pb2.TimeFilterFastResponse()  # type: ignore
        response_body.ParseFromString(content)
        return TimeFilterProtoResponse(
            travel_times=response_body.properties.travelTimes[:],
            distances=response_body.properties.distances[:],
        )
