from typing import Dict

from dacite import from_dict

from traveltime import AcceptType
from traveltime.requests import *
from traveltime.responses import TimeMapResponse, MapInfo
from traveltime.utils import send_request


class TravelTimeSdk:

    def __init__(self, app_id: str, api_key: str) -> None:
        self.__app_id = app_id
        self.__api_key = api_key

    def map_info(self):
        response = send_request(path='map-info', headers=self.__headers(AcceptType.JSON))
        return from_dict(data_class=MapInfo, data=response)

    def time_map(
        self,
        arrival_searches: List[ArrivalSearch] = None,
        departure_searches: List[DepartureSearch] = None,
        unions: List[Union] = None,
        intersections: List[Intersection] = None
    ) -> TimeMapResponse:
        response = send_request(
            path='time-map',
            headers=self.__headers(AcceptType.JSON),
            body=TimeMapRequest(departure_searches, arrival_searches, unions, intersections)
        )
        return from_dict(data_class=TimeMapResponse, data=response)

   # async def time_map_async(self,arrival_searches: List[ArrivalSearch] = None, departure_searches: List[DepartureSearch] = None,unions: List[Union] = None,intersections: List[Intersection] = None) -> TimeMapResponse:

    def __headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            'X-Application-Id': self.__app_id,
            'X-Api-Key': self.__api_key,
            'Content-Type': 'application/json',
            'Accept': accept_type.value
        }
