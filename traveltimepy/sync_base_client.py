import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Optional, Dict, TypeVar, Type, List, Union, cast

import requests
from pydantic import BaseModel, ValidationError
from requests.auth import HTTPBasicAuth
from requests_ratelimiter import LimiterSession
from tenacity import (
    retry,
    stop_after_attempt,
    wait_none,
    retry_if_exception_type,
)

from traveltimepy.accept_type import AcceptType
from traveltimepy.base_client import (
    BaseClient,
    __version__,
    check_protobuf_available,
    parse_geohash_proto_response,
    parse_h3_proto_response,
    parse_time_filter_proto_response,
)
from traveltimepy.errors import (
    TravelTimeError,
    TravelTimeJsonError,
    TravelTimeServerError,
)
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.requests.time_filter_proto import (
    TimeFilterFastProtoRequest,
)
from traveltimepy.requests.geohash_fast_proto import (
    GeohashFastProtoRequest,
)
from traveltimepy.requests.h3_fast_proto import (
    H3FastProtoRequest,
)
from traveltimepy.responses.error import ResponseError
from traveltimepy.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.responses.geohash_fast_proto import GeohashFastProtoResponse
from traveltimepy.responses.h3_fast_proto import H3FastProtoResponse

T = TypeVar("T", bound=BaseModel)


class SyncBaseClient(BaseClient):
    """
    Args:
        app_id: Your TravelTime API application ID
        api_key: Your TravelTime API key
        timeout: Request timeout in seconds (default: 300)
        retry_attempts: Number of retry attempts for 5xx server errors (default: 3)
        max_rpm: Maximum requests per minute for rate limiting (default: 60)
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
        use_ssl: bool = True,
        split_large_requests: bool = True,
        _host: str = "api.traveltimeapp.com",
        _proto_host: str = "proto.api.traveltimeapp.com",
        _user_agent: str = f"Travel Time Python SDK {__version__}",
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

        self._session = self._create_rate_limited_session(max_rpm)

    def close(self):
        """Close the requests session if it exists."""
        if self._session:
            self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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
        @retry(
            retry=retry_if_exception_type(TravelTimeServerError),
            stop=stop_after_attempt(
                self.retry_attempts + 1
            ),  # First attempt is not a retry, that's why `+1`
            wait=wait_none(),  # No wait between retries
        )
        def _make_request_with_retry():
            response = self._session.request(
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

        return _make_request_with_retry()

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
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> T:
        url = self._build_url(endpoint)
        headers = {**self._get_json_headers(accept_type), **(extra_headers or {})}

        return self._make_request(
            method="GET",
            url=url,
            headers=headers,
            response_class=response_class,
            params=params,
        )

    def _proto_call(
        self,
        req: Union[
            TimeFilterFastProtoRequest, GeohashFastProtoRequest, H3FastProtoRequest
        ],
        endpoint: str,
        parse: Callable[[bytes], T],
    ) -> T:
        check_protobuf_available()

        @retry(
            retry=retry_if_exception_type(TravelTimeServerError),
            stop=stop_after_attempt(
                self.retry_attempts + 1
            ),  # First attempt is not a retry, that's why `+1`
            wait=wait_none(),  # No wait between retries
        )
        def _make_proto_request() -> T:
            transportation_mode = self._get_transportation_mode(req.transportation)

            url = f"https://{self._proto_host}/api/v3/{req.country.value}/{endpoint}/fast/{transportation_mode}"
            headers = self._get_proto_headers()
            auth = HTTPBasicAuth(self.app_id, self.api_key)
            data = req.get_request().SerializeToString()

            response = self._session.post(
                url=url,
                headers=headers,
                data=data,
                auth=auth,
                timeout=self.timeout,
                verify=self.use_ssl,
            )

            if response.status_code != 200:
                self._handle_proto_error(response.status_code, response.headers)
            return parse(response.content)

        return _make_proto_request()

    def _api_call_proto(
        self, req: TimeFilterFastProtoRequest
    ) -> TimeFilterProtoResponse:
        return self._proto_call(req, "time-filter", parse_time_filter_proto_response)

    def _api_call_geohash_proto(
        self, req: GeohashFastProtoRequest
    ) -> GeohashFastProtoResponse:
        return self._proto_call(req, "geohash", parse_geohash_proto_response)

    def _api_call_h3_proto(self, req: H3FastProtoRequest) -> H3FastProtoResponse:
        return self._proto_call(req, "h3", parse_h3_proto_response)

    def _handle_response(
        self, response: requests.Response, response_class: Type[T]
    ) -> T:
        try:
            json_data = response.json()
        except requests.exceptions.JSONDecodeError:
            json_data = {"error": "Invalid JSON response"}

        if response.status_code != 200:
            try:
                error = ResponseError.model_validate_json(json.dumps(json_data))
            except ValidationError:
                raise TravelTimeError(
                    f"Server returned status code {response.status_code} "
                    f"with unexpected response: {json_data}"
                )
            if response.status_code >= 500:
                raise TravelTimeServerError(error.description)
            else:
                raise TravelTimeJsonError(
                    status_code=response.status_code,
                    error_code=str(error.error_code),
                    description=error.description,
                    documentation_link=error.documentation_link,
                    additional_info=error.additional_info,
                )
        else:
            return response_class.model_validate(json_data)
