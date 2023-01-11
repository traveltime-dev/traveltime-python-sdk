from datetime import datetime
from typing import Dict, Union, List, Optional, Tuple

from traveltime.errors import ApiError

from traveltimepy.dto import Location, LocationId
from traveltimepy.dto.requests import FullRange, Property, to_list
from traveltimepy.dto.requests.time_filter import TimeFilterRequest
from traveltimepy.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
from traveltimepy.dto.requests import (
    time_filter as time_filter_package
)


def create_time_filter(
    locations: List[Location],
    searches: Dict[LocationId, List[LocationId]],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    properties: Optional[List[Property]],
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    travel_time: int,
    full_range: Optional[FullRange]
) -> TimeFilterRequest:
    if properties is None:
        properties = [Property.TRAVEL_TIME]
    if arrival_time is not None:
        return TimeFilterRequest(
            locations=locations,
            arrival_searches=[
                time_filter_package.ArrivalSearch(
                    id=arrival_id,
                    arrival_location_id=arrival_id,
                    departure_location_ids=[departure_id for departure_id in departure_ids],
                    arrival_time=arrival_time,
                    travel_time=travel_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for arrival_id, departure_ids in searches.items()
            ],
            departure_searches=[]
        )
    elif departure_time is not None:
        return TimeFilterRequest(
            locations=locations,
            departure_searches=[
                time_filter_package.DepartureSearch(
                    id=departure_id,
                    departure_location_id=departure_id,
                    arrival_location_ids=[arrival_id for arrival_id in arrival_ids],
                    departure_time=departure_time,
                    travel_time=travel_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for departure_id, arrival_ids in searches.items()
            ],
            arrival_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specify')
