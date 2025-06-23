import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, TypeVar, Type, List, cast

import requests
from pydantic import BaseModel
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from requests_ratelimiter import LimiterSession
from urllib3.util.retry import Retry

import TimeFilterFastResponse_pb2  # type: ignore
from traveltimepy.accept_type import AcceptType
from traveltimepy.base_client import BaseClient, __version__
from traveltimepy.errors import (
    TravelTimeJsonError,
    TravelTimeProtoError,
)
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.requests.time_filter_proto import (
    TimeFilterFastProtoRequest,
    ProtoTransportation,
)
from traveltimepy.responses.error import ResponseError
from traveltimepy.responses.time_filter_proto import TimeFilterProtoResponse

T = TypeVar("T", bound=BaseModel)


class SyncBaseClient(BaseClient):
    """
    Args:
        app_id: Your TravelTime API application ID
        api_key: Your TravelTime API key
        timeout: Request timeout in seconds (default: 300)
        retry_attempts: Number of retry attempts for failed requests (default: 3)
        max_rpm: Maximum requests per minute for rate limiting (default: 60)
        session: Optional existing aiohttp ClientSession to use
        use_ssl: Whether to use SSL for connections (default: True)
        split_large_requests: Split large requests into smaller requests for performance (default: True)
        _host: API host (default: "api.traveltimeapp.com")
        _proto_host: Proto API host (default: "proto.api.traveltimeapp.com")
        _user_agent: User agent string for requests
    """

    def __init__(
        self,
        app_id: str,
        api_key: str,
        timeout: int = 300,
        retry_attempts: int = 3,
        max_rpm: int = 60,
        session: Optional[requests.Session] = None,
        use_ssl: bool = True,
        split_large_requests: bool = True,
        _host: str = "api.traveltimeapp.com",
        _proto_host: str = "proto.api.traveltimeapp.com",
        _user_agent: str = f"Travel Time Python SDK {__version__}",
        _split_size: int = 10,  # Splits requests to improve performance
    ):
        super().__init__(
            app_id=app_id,
            api_key=api_key,
            timeout=timeout,
            retry_attempts=retry_attempts,
            max_rpm=max_rpm,
            use_ssl=use_ssl,
            split_large_requests=split_large_requests,
            _host=_host,
            _proto_host=_proto_host,
            _user_agent=_user_agent,
        )

        if session:
            self.session = session
        else:
            self.session = self._create_rate_limited_session(max_rpm)

    def _create_rate_limited_session(
        self,
        per_minute: float = 0,
    ) -> LimiterSession:
        session = LimiterSession(
            per_minute=per_minute,
            # Automatically handle rate limit responses
            limit_statuses=[429],
            per_host=True,
        )

        retry_strategy = Retry(
            total=self.retry_attempts,
            backoff_factor=1,
            status_forcelist=[
                500,
                503,
                504,
            ],  # Don't retry 429 - let rate limiter handle it
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _make_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        response_class: Type[T],
        data: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
        auth: Optional[HTTPBasicAuth] = None,
    ) -> T:
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
            auth=auth,
            timeout=self.timeout,
            verify=self.use_ssl,
        )

        return self._handle_response(response, response_class)

    def _api_call_post(
        self,
        response_class: Type[T],
        endpoint: str,
        accept_type: AcceptType,
        request: TravelTimeRequest,
    ) -> T:
        url = self._build_url(endpoint)
        headers = self._get_json_headers(accept_type)

        split_size = 10 if self.split_large_requests else 1

        # Split requests and process concurrently
        parts = request.split_searches(split_size)

        if len(parts) == 1:
            # Single request - no need for threading overhead
            return self._make_request(
                method="POST",
                url=url,
                headers=headers,
                response_class=response_class,
                data=parts[0].model_dump_json(),
            )

        # Multiple parts - send concurrently
        responses = []
        max_workers = min(len(parts), split_size)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_index = {
                executor.submit(
                    self._make_request,
                    method="POST",
                    url=url,
                    headers=headers,
                    response_class=response_class,
                    data=part.model_dump_json(),
                ): i
                for i, part in enumerate(parts)
            }

            indexed_responses: List[T] = cast(List[T], [None] * len(parts))
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                indexed_responses[index] = future.result()

            responses = indexed_responses

        return request.merge(responses)

    def _api_call_get(
        self,
        response_class: Type[T],
        endpoint: str,
        accept_type: AcceptType,
        params: Optional[Dict[str, str]],
    ) -> T:
        url = self._build_url(endpoint)
        headers = self._get_json_headers(accept_type)

        return self._make_request(
            method="GET",
            url=url,
            headers=headers,
            response_class=response_class,
            params=params,
        )

    def _api_call_proto(
        self, req: TimeFilterFastProtoRequest
    ) -> TimeFilterProtoResponse:
        if isinstance(req.transportation, ProtoTransportation):
            transportation_mode = req.transportation.value.name
        else:
            transportation_mode = req.transportation.TYPE.value.name

        url = f"https://{self._proto_host}/api/v2/{req.country.value}/time-filter/fast/{transportation_mode}"
        headers = self._get_proto_headers()
        auth = HTTPBasicAuth(self.app_id, self.api_key)
        data = req.get_request().SerializeToString()

        response = self.session.post(
            url=url,
            headers=headers,
            data=data,
            auth=auth,
            timeout=self.timeout,
            verify=self.use_ssl,
        )

        if response.status_code != 200:
            raise TravelTimeProtoError(
                status_code=response.status_code,
                error_code=response.headers.get("X-ERROR-CODE", "Unknown"),
                error_details=response.headers.get(
                    "X-ERROR-DETAILS", "No details provided"
                ),
                error_message=response.headers.get(
                    "X-ERROR-MESSAGE", "No message provided"
                ),
            )
        else:
            response_body = TimeFilterFastResponse_pb2.TimeFilterFastResponse()  # type: ignore
            response_body.ParseFromString(response.content)
            return TimeFilterProtoResponse(
                travel_times=response_body.properties.travelTimes[:],
                distances=response_body.properties.distances[:],
            )

    def _handle_response(
        self, response: requests.Response, response_class: Type[T]
    ) -> T:
        try:
            json_data = response.json()
        except requests.exceptions.JSONDecodeError:
            json_data = {"error": "Invalid JSON response"}

        if response.status_code != 200:
            error = ResponseError.model_validate_json(json.dumps(json_data))
            raise TravelTimeJsonError(
                status_code=response.status_code,
                error_code=str(error.error_code),
                description=error.description,
                documentation_link=error.documentation_link,
                additional_info=error.additional_info,
            )
        else:
            return response_class.model_validate(json_data)

    def close(self):
        if hasattr(self, "session"):
            self.session.close()
