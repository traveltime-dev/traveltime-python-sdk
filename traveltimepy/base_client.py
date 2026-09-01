from importlib.metadata import version, PackageNotFoundError
from typing import Dict, Mapping, Union, Any

from traveltimepy.accept_type import AcceptType
from traveltimepy.errors import TravelTimeProtoError, TravelTimeServerError
from traveltimepy.requests.time_filter_proto import ProtoTransportation
from traveltimepy.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.responses.geohash_fast_proto import GeohashFastProtoResponse
from traveltimepy.responses.h3_fast_proto import H3FastProtoResponse

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

try:
    from traveltimepy.proto import TimeFilterFastResponse_pb2  # type: ignore
    from traveltimepy.proto import GeohashFastResponse_pb2  # type: ignore
    from traveltimepy.proto import H3FastResponse_pb2  # type: ignore

    PROTOBUF_AVAILABLE = True
except ImportError:
    PROTOBUF_AVAILABLE = False
    TimeFilterFastResponse_pb2 = None  # type: ignore
    GeohashFastResponse_pb2 = None  # type: ignore
    H3FastResponse_pb2 = None  # type: ignore


def check_protobuf_available() -> None:
    if not PROTOBUF_AVAILABLE:
        raise ImportError(
            "protobuf is required for proto API calls. "
            "Install it with: pip install 'traveltimepy[proto]'"
        )


def parse_time_filter_proto_response(content: bytes) -> TimeFilterProtoResponse:
    response_body = TimeFilterFastResponse_pb2.TimeFilterFastResponse()  # type: ignore
    response_body.ParseFromString(content)
    return TimeFilterProtoResponse(
        travel_times=response_body.properties.travelTimes[:],
        distances=response_body.properties.distances[:],
        monthly_fares=response_body.properties.monthlyFares[:],
    )


def parse_geohash_proto_response(content: bytes) -> GeohashFastProtoResponse:
    response_body = GeohashFastResponse_pb2.GeohashFastResponse()  # type: ignore
    response_body.ParseFromString(content)
    return GeohashFastProtoResponse(
        ids=response_body.cells.ids[:],
        min_travel_times=response_body.cells.minTravelTimes[:],
        max_travel_times=response_body.cells.maxTravelTimes[:],
        mean_travel_times=response_body.cells.meanTravelTimes[:],
    )


def parse_h3_proto_response(content: bytes) -> H3FastProtoResponse:
    response_body = H3FastResponse_pb2.H3FastResponse()  # type: ignore
    response_body.ParseFromString(content)
    return H3FastProtoResponse(
        ids=[format(cell_id, "x") for cell_id in response_body.cells.ids],
        min_travel_times=response_body.cells.minTravelTimes[:],
        max_travel_times=response_body.cells.maxTravelTimes[:],
        mean_travel_times=response_body.cells.meanTravelTimes[:],
    )


class BaseClient:

    def __init__(
        self,
        app_id: str,
        api_key: str,
        timeout: int = 300,
        retry_attempts: int = 3,
        max_rpm: int = 60,
        use_ssl: bool = True,
        split_large_requests: bool = True,
        _host: str = "api.traveltimeapp.com",
        _proto_host: str = "proto.api.traveltimeapp.com",
        _user_agent: str = f"Travel Time Python SDK {__version__}",
    ):
        self.app_id = app_id
        self.api_key = api_key
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.max_rpm = max_rpm
        self.use_ssl = use_ssl
        self.split_large_requests = split_large_requests
        self._host = _host
        self._proto_host = _proto_host
        self._user_agent = _user_agent

    def _build_url(self, endpoint: str) -> str:
        return f"https://{self._host}/v4/{endpoint}"

    def _get_json_headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            "X-Application-Id": self.app_id,
            "X-Api-Key": self.api_key,
            "User-Agent": self._user_agent,
            "Content-Type": "application/json",
            "Accept": accept_type.value,
        }

    def _get_proto_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": AcceptType.OCTET_STREAM.value,
            "User-Agent": self._user_agent,
        }

    @staticmethod
    def _get_transportation_mode(
        transportation: Union[ProtoTransportation, Any],
    ) -> str:
        if isinstance(transportation, ProtoTransportation):
            return transportation.value.name
        else:
            return transportation.TYPE.value.name

    @staticmethod
    def _handle_proto_error(status_code: int, headers: Mapping[str, str]) -> None:
        if status_code >= 500:
            raise TravelTimeServerError("Internal server error")
        else:
            raise TravelTimeProtoError(
                status_code=status_code,
                error_code=headers.get("X-ERROR-CODE", "Unknown"),
                error_details=headers.get("X-ERROR-DETAILS", "No details provided"),
                error_message=headers.get("X-ERROR-MESSAGE", "No message provided"),
            )
