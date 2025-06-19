from abc import ABC, abstractmethod
from importlib.metadata import version, PackageNotFoundError
from typing import Optional, Dict, TypeVar, Type, Union, Coroutine, Any, Mapping

from pydantic import BaseModel

from traveltimepy.accept_type import AcceptType
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.requests.time_filter_proto import (
    TimeFilterFastProtoRequest,
)
from traveltimepy.responses.error import ResponseError
from traveltimepy.responses.time_filter_proto import TimeFilterProtoResponse

T = TypeVar("T", bound=BaseModel)

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"


class BaseClient(ABC):

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
            "User-Agent": f"Travel Time Python SDK {__version__}",
        }

    def _build_proto_error_message(
        self, status_code: int, headers: Mapping[str, str]
    ) -> str:
        error_code = headers.get("X-ERROR-CODE", "Unknown")
        error_details = headers.get("X-ERROR-DETAILS", "No details provided")
        error_message = headers.get("X-ERROR-MESSAGE", "No message provided")

        return (
            f"Travel Time API proto request failed with error code: {status_code}\n"
            f"X-ERROR-CODE: {error_code}\n"
            f"X-ERROR-DETAILS: {error_details}\n"
            f"X-ERROR-MESSAGE: {error_message}"
        )

    def _build_api_error_message(self, parsed: ResponseError) -> str:
        return (
            f"Travel Time API request failed: {parsed.description}\n"
            f"Error code: {parsed.error_code}\n"
            f"Additional info: {parsed.additional_info}\n"
            f"<{parsed.documentation_link}>\n"
        )

    @abstractmethod
    def _api_call_post(
        self,
        response_class: Type[T],
        endpoint: str,
        accept_type: AcceptType,
        request: TravelTimeRequest,
    ) -> Union[T, Coroutine[Any, Any, T]]:
        pass

    @abstractmethod
    def _api_call_get(
        self,
        response_class: Type[T],
        endpoint: str,
        accept_type: AcceptType,
        params: Optional[Dict[str, str]],
    ) -> Union[T, Coroutine[Any, Any, T]]:
        pass

    @abstractmethod
    def _api_call_proto(
        self, req: TimeFilterFastProtoRequest
    ) -> Union[TimeFilterProtoResponse, Coroutine[Any, Any, TimeFilterProtoResponse]]:
        pass
