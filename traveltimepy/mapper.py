from datetime import datetime
from typing import Dict, Union, List, Optional, Tuple

from traveltime.errors import ApiError

from traveltimepy.dto import Location
from traveltimepy.dto.requests import FullRange, Property, to_list
from traveltimepy.dto.requests.time_filter import TimeFilterRequest
from traveltimepy.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
from traveltimepy.dto.requests import (
    time_filter as time_filter_package
)


def create_time_filter_request(
    locations: Dict[Location, List[Location]],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    properties: Optional[List[Property]],
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    travel_time: int,
    full_range: Optional[FullRange]
) -> TimeFilterRequest:
    all_locations = to_list(locations)
    if properties is None:
        properties = [Property.TRAVEL_TIME]
    if arrival_time is not None:
        return TimeFilterRequest(
            locations=all_locations,
            arrival_searches=[
                time_filter_package.ArrivalSearch(
                    id=arrival.id,
                    arrival_location_id=arrival.id,
                    departure_location_ids=[departure.id for departure in departures],
                    arrival_time=arrival_time,
                    travel_time=travel_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for arrival, departures in locations.items()
            ],
            departure_searches=[]
        )
    elif departure_time is not None:
        return TimeFilterRequest(
            locations=all_locations,
            departure_searches=[
                time_filter_package.DepartureSearch(
                    id=departure.id,
                    departure_location_id=departure.id,
                    arrival_location_ids=[arrival.id for arrival in arrivals],
                    arrival_time=arrival_time,
                    travel_time=travel_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for departure, arrivals in locations.items()
            ],
            arrival_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specify')
