from datetime import datetime
from typing import Dict, Union, List, Optional

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
    properties: List[Property],
    departure_time: Optional[datetime] = None,
    arrival_time: Optional[datetime] = None,
    travel_time: int = 3600,
    full_range: Optional[FullRange] = None
) -> TimeFilterRequest:
    all_locations = to_list(locations)
    if arrival_time is not None:
        arrival_searches = [
            time_filter_package.ArrivalSearch(
                id="Search from" + arrival.id,
                arrival_location_id=arrival.id,
                departure_location_ids=[departure.id for departure in departures],
                arrival_time=arrival_time,
                travel_time=travel_time,
                transportation=transportation,
                properties=properties,
                full_range=full_range
            )
            for arrival, departures in locations.items()
        ]
        return TimeFilterRequest(
            locations=all_locations,
            arrival_searches=arrival_searches,
            departure_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specify')
