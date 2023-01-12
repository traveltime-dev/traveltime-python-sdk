from traveltimepy.dto.requests.time_filter_proto import TimeFilterProtoRequest
from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse


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