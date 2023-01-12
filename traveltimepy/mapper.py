from datetime import datetime
from typing import Dict, Union, List, Optional

from traveltime.errors import ApiError

from traveltimepy.dto import Location, LocationId, Coordinates
from traveltimepy.dto.requests import FullRange, Property
from traveltimepy.dto.requests.postcodes import PostcodesRequest
from traveltimepy.dto.requests.routes import RoutesRequest
from traveltimepy.dto.requests.time_filter import TimeFilterRequest
from traveltimepy.dto.requests.time_filter_fast import TimeFilterFastRequest, Transportation, OneToMany, ManyToOne
from traveltimepy.dto.requests.zones import ZonesProperty, DistrictsRequest, SectorsRequest
from traveltimepy.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
from traveltimepy.dto.requests import (
    time_filter as time_filter_package,
    time_filter_fast as time_filter_fast_package,
    postcodes as postcodes_package,
    zones as zones_package,
    routes as routes_package
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
        raise ApiError('arrival_time or departure_time should be specified')


def create_time_filter_fast(
    locations: List[Location],
    searches: Dict[LocationId, List[LocationId]],
    transportation: Transportation,
    travel_time: int = 3600,
    properties: Optional[List[Property]] = None,
    one_to_many: bool = False
) -> TimeFilterFastRequest:
    if properties is None:
        properties = [Property.TRAVEL_TIME]
    if one_to_many:
        return TimeFilterFastRequest(
            locations=locations,
            arrival_searches=time_filter_fast_package.ArrivalSearches(
                one_to_many=[
                    OneToMany(
                        id=departure_id,
                        departure_location_id=departure_id,
                        arrival_location_ids=arrival_ids,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period='weekday_morning',
                        properties=properties
                    )
                    for departure_id, arrival_ids in searches.items()
                ],
                many_to_one=[]
            )
        )
    else:
        return TimeFilterFastRequest(
            locations=locations,
            arrival_searches=time_filter_fast_package.ArrivalSearches(
                many_to_one=[
                    ManyToOne(
                        id=arrival_id,
                        arrival_location_id=arrival_id,
                        departure_location_ids=departure_ids,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period='weekday_morning',
                        properties=properties
                    )
                    for arrival_id, departure_ids in searches.items()
                ],
                one_to_many=[]
            )
        )


def create_postcodes(
    coordinates: List[Coordinates],
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    travel_time: int,
    properties: Optional[List[Property]],
    full_range: Optional[FullRange]
) -> PostcodesRequest:
    if properties is None:
        properties = [Property.TRAVEL_TIME]

    if departure_time is not None:
        return PostcodesRequest(
            departure_searches=[
                postcodes_package.DepartureSearch(
                    id=f'Search for Coordinate({cur_coordinates.lat}, {cur_coordinates.lng})',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=departure_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for cur_coordinates in coordinates
            ],
            arrival_searches=[]
        )
    elif arrival_time is not None:
        return PostcodesRequest(
            arrival_searches=[
                postcodes_package.ArrivalSearch(
                    id=f'Search for Coordinate({cur_coordinates.lat}, {cur_coordinates.lng})',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=arrival_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for cur_coordinates in coordinates
            ],
            departure_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')


def create_districts(
    coordinates: List[Coordinates],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    travel_time: int,
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    reachable_postcodes_threshold,
    properties: Optional[List[ZonesProperty]],
    full_range: Optional[FullRange]
) -> DistrictsRequest:
    if properties is None:
        properties = ZonesProperty.TRAVEL_TIME_ALL
    if arrival_time is not None:
        return DistrictsRequest(
            arrival_searches=[
                zones_package.ArrivalSearch(
                    id=f'Search for Coordinate({cur_coordinates.lat}, {cur_coordinates.lng})',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=arrival_time,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for cur_coordinates in coordinates
            ],
            departure_searches=[]
        )
    elif departure_time is not None:
        return DistrictsRequest(
            arrival_searches=[
                zones_package.ArrivalSearch(
                    id=f'Search for Coordinate({cur_coordinates.lat}, {cur_coordinates.lng})',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=departure_time,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for cur_coordinates in coordinates
            ],
            departure_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')


def create_sectors(
    coordinates: List[Coordinates],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    travel_time: int,
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    reachable_postcodes_threshold,
    properties: Optional[List[ZonesProperty]],
    full_range: Optional[FullRange]
) -> SectorsRequest:
    if properties is None:
        properties = ZonesProperty.TRAVEL_TIME_ALL
    if arrival_time is not None:
        return SectorsRequest(
            arrival_searches=[
                zones_package.ArrivalSearch(
                    id=f'Search for Coordinate({cur_coordinates.lat}, {cur_coordinates.lng})',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=arrival_time,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for cur_coordinates in coordinates
            ],
            departure_searches=[]
        )
    elif departure_time is not None:
        return SectorsRequest(
            arrival_searches=[
                zones_package.ArrivalSearch(
                    id=f'Search for Coordinate({cur_coordinates.lat}, {cur_coordinates.lng})',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=departure_time,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for cur_coordinates in coordinates
            ],
            departure_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')


def create_routes(
    locations: List[Location],
    searches: Dict[LocationId, List[LocationId]],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    properties: Optional[List[Property]],
    full_range: Optional[FullRange]
) -> RoutesRequest:
    if properties is None:
        properties = [Property.TRAVEL_TIME]
    if arrival_time is not None:
        return RoutesRequest(
            locations=locations,
            arrival_searches=[
                routes_package.ArrivalSearch(
                    id=arrival_id,
                    arrival_location_id=arrival_id,
                    departure_location_ids=[departure_id for departure_id in departure_ids],
                    arrival_time=arrival_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for arrival_id, departure_ids in searches.items()
            ],
            departure_searches=[]
        )
    elif departure_time is not None:
        return RoutesRequest(
            locations=locations,
            departure_searches=[
                routes_package.DepartureSearch(
                    id=departure_id,
                    departure_location_id=departure_id,
                    arrival_location_ids=[arrival_id for arrival_id in arrival_ids],
                    departure_time=departure_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for departure_id, arrival_ids in searches.items()
            ],
            arrival_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')
