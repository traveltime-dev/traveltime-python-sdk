from dacite import from_dict

from traveltime.requests import *
from traveltime.responses import TimeMapResponse
from traveltime.utils import send_request


class TravelTimeSdk:

    def __init__(self, app_id: str, api_key: str) -> None:
        self.__headers = {
            'X-Application-Id': app_id,
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        }

    def map_info(self):
        """Map Info

        Returns information about currently supported countries.
        See https://traveltime.com/docs/api/reference/map-info for details

        Returns:
            dict: API response parsed as a dictionary
        """
        return send_request(path='map-info', headers=self.__headers)

    def time_map(
        self,
        arrival_searches: List[ArrivalSearch] = None,
        departure_searches: List[DepartureSearch] = None,
        unions: List[Union] = None,
        intersections: List[Intersection] = None
    ) -> TimeMapResponse:
        request = TimeMapRequest(departure_searches, arrival_searches, unions, intersections)
        response = send_request(path='time-map', headers=self.__headers, body=request)
        return from_dict(data_class=TimeMapResponse, data=response)
