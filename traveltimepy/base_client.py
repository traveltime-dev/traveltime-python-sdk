from importlib.metadata import version, PackageNotFoundError
from typing import Dict, Mapping, Union, Any

from traveltimepy.accept_type import AcceptType
from traveltimepy.errors import TravelTimeProtoError, TravelTimeServerError
from traveltimepy.requests.time_filter_proto import ProtoTransportation

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"


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
