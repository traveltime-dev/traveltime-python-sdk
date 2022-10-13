import dataclasses
import json
from typing import TypeVar, List

import requests
from requests import Response

from traveltime.errors import ApiError
from traveltime.requests import *
from traveltime.responses import TimeMapResponse
from traveltime.utils import send_request

T = TypeVar('T')
R = TypeVar('R')


class TravelTimeSdk:

    def __init__(self, app_id: str, api_key: str) -> None:
        self.__headers = {'X-Application-Id': app_id, 'X-Api-Key': api_key, 'User-Agent': 'Travel Time Python SDK'}

    def map_info(self):
        """Map Info

        Returns information about currently supported countries.
        See https://traveltime.com/docs/api/reference/map-info for details

        Returns:
            dict: API response parsed as a dictionary
        """
        return send_request(path='map-info', params=None, headers=self.__headers)

    def time_map(
        self,
        arrival_searches: List[ArrivalSearch],
        departure_searches: List[DepartureSearch],
        unions: List[Union],
        intersections: List[Intersection]
    ) -> TimeMapResponse:
        request = TimeMapRequest(departure_searches, arrival_searches, unions, intersections)
        return send_request(path='time-map', headers=self.__headers, body=request)
