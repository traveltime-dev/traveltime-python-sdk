from traveltime import AcceptType
from traveltime.dto import Location
from traveltime.dto.requests import time_map_request, time_filter_request
from traveltime.dto.requests.time_filter_request import TimeFilterRequest

from traveltime.dto.requests.time_map_request import *
from traveltime.dto.responses.map_info_response import MapInfoResponse
from traveltime.dto.responses.time_filter_response import TimeFilterResponse
from traveltime.dto.responses.time_map_response import TimeMapResponse
from traveltime.utils import *


class TravelTimeSdk:

    def __init__(self, app_id: str, api_key: str) -> None:
        self.__app_id = app_id
        self.__api_key = api_key

    def map_info(self) -> MapInfoResponse:
        return send_get_request(MapInfoResponse, 'map-info', self.__headers(AcceptType.JSON))

    async def map_info_async(self) -> MapInfoResponse:
        return await send_get_request_async(MapInfoResponse, 'map-info', self.__headers(AcceptType.JSON))

    def time_map(
        self,
        arrival_searches: List[time_map_request.ArrivalSearch],
        departure_searches: List[time_map_request.DepartureSearch],
        unions: List[Union] = None,
        intersections: List[Intersection] = None
    ) -> TimeMapResponse:
        request = TimeMapRequest(
            departure_searches=departure_searches,
            arrival_searches=arrival_searches,
            unions=unions,
            intersections=intersections
        )
        return send_post_request(TimeMapResponse, 'time-map', self.__headers(AcceptType.JSON), request)

    async def time_map_async(
        self,
        arrival_searches: List[ArrivalSearch] = None,
        departure_searches: List[DepartureSearch] = None,
        unions: List[Union] = None,
        intersections: List[Intersection] = None
    ) -> TimeMapResponse:
        request = TimeMapRequest(
            departure_searches=departure_searches,
            arrival_searches=arrival_searches,
            unions=unions,
            intersections=intersections
        )
        return await send_post_request_async(TimeMapResponse, 'time-map', self.__headers(AcceptType.JSON), request)

    def time_filter(
        self,
        locations: List[Location],
        departure_searches: List[time_map_request.DepartureSearch],
        arrival_searches: List[time_map_request.ArrivalSearch]
    ) -> TimeFilterResponse:
        request = TimeFilterRequest(locations, departure_searches, arrival_searches)
        return send_post_request(TimeFilterResponse, 'time-filter', self.__headers(AcceptType.JSON), request)

    async def time_filter_async(
        self,
        locations: List[Location],
        departure_searches: List[time_filter_request.DepartureSearch],
        arrival_searches: List[time_filter_request.ArrivalSearch]
    ) -> TimeFilterResponse:
        request = TimeFilterRequest(locations, departure_searches, arrival_searches)
        return await send_post_request_async(TimeFilterResponse, 'time-filter', self.__headers(AcceptType.JSON), request)

    def __headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            'X-Application-Id': self.__app_id,
            'X-Api-Key': self.__api_key,
            'Content-Type': 'application/json',
            'Accept': accept_type.value
        }
