from typing import Dict

from aiohttp import ClientSession, ClientResponse, BasicAuth, TCPConnector

from traveltimepy.TimeFilterFastResponse_pb2 import TimeFilterFastResponse
from traveltimepy.TimeFilterFastRequest_pb2 import TimeFilterFastRequest
from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.errors import ApiError


async def send_proto_async(
    url: str,
    headers: Dict[str, str],
    data: TimeFilterFastRequest,
    app_id: str,
    api_key: str,
) -> TimeFilterFastResponse:
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
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
        msg = (
            f"Travel Time API proto request failed with error code: {response.status}\n"
        )
        raise ApiError(msg)
    else:
        response_body = TimeFilterFastResponse()
        response_body.ParseFromString(content)
        return TimeFilterProtoResponse(
            travel_times=response_body.properties.travelTimes[:]
        )
