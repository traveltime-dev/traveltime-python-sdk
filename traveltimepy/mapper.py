import math
from datetime import datetime
from typing import Dict, Union, List, Optional

from traveltimepy.errors import ApiError
from traveltimepy import TimeFilterFastRequest_pb2

from traveltimepy.dto.common import Location, Coordinates, FullRange, Property, Range
from traveltimepy.dto.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
from traveltimepy.dto.requests.time_filter_fast import Transportation
from traveltimepy.dto.requests.zones import ZonesProperty

from traveltimepy.dto.requests.postcodes import PostcodesRequest
from traveltimepy.dto.requests.routes import RoutesRequest
from traveltimepy.dto.requests.time_filter import TimeFilterRequest
from traveltimepy.dto.requests.time_filter_fast import TimeFilterFastRequest
from traveltimepy.dto.requests.time_filter_proto import ProtoTransportation
from traveltimepy.dto.requests.zones import DistrictsRequest, SectorsRequest
from traveltimepy.dto.requests.time_map import TimeMapRequest


from traveltimepy.dto.requests import (
    time_filter,
    time_filter_fast,
    postcodes,
    zones,
    routes,
    time_map
)


def create_time_filter(
    locations: List[Location],
    search_ids: Dict[str, List[str]],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    properties: Optional[List[Property]],
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    travel_time: int,
    full_range: Optional[FullRange]
) -> TimeFilterRequest:
    if properties is None:
        properties = [Property.TRAVEL_TIME]
    if arrival_time is not None and departure_time is not None:
        raise ApiError('arrival_time and departure_time cannot be both specified')

    if arrival_time is not None:
        return TimeFilterRequest(
            locations=locations,
            arrival_searches=[
                time_filter.ArrivalSearch(
                    id=arrival_id,
                    arrival_location_id=arrival_id,
                    departure_location_ids=[departure_id for departure_id in departure_ids],
                    arrival_time=arrival_time,
                    travel_time=travel_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for arrival_id, departure_ids in search_ids.items()
            ],
            departure_searches=[]
        )
    elif departure_time is not None:
        return TimeFilterRequest(
            locations=locations,
            departure_searches=[
                time_filter.DepartureSearch(
                    id=departure_id,
                    departure_location_id=departure_id,
                    arrival_location_ids=[arrival_id for arrival_id in arrival_ids],
                    departure_time=departure_time,
                    travel_time=travel_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for departure_id, arrival_ids in search_ids.items()
            ],
            arrival_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')


def create_time_filter_fast(
    locations: List[Location],
    search_ids: Dict[str, List[str]],
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
            arrival_searches=time_filter_fast.ArrivalSearches(
                one_to_many=[
                    time_filter_fast.OneToMany(
                        id=departure_id,
                        departure_location_id=departure_id,
                        arrival_location_ids=arrival_ids,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period='weekday_morning',
                        properties=properties
                    )
                    for departure_id, arrival_ids in search_ids.items()
                ],
                many_to_one=[]
            )
        )
    else:
        return TimeFilterFastRequest(
            locations=locations,
            arrival_searches=time_filter_fast.ArrivalSearches(
                many_to_one=[
                    time_filter_fast.ManyToOne(
                        id=arrival_id,
                        arrival_location_id=arrival_id,
                        departure_location_ids=departure_ids,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period='weekday_morning',
                        properties=properties
                    )
                    for arrival_id, departure_ids in search_ids.items()
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

    if arrival_time is not None and departure_time is not None:
        raise ApiError('arrival_time and departure_time cannot be both specified')

    if departure_time is not None:
        return PostcodesRequest(
            departure_searches=[
                postcodes.DepartureSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=departure_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[]
        )
    elif arrival_time is not None:
        return PostcodesRequest(
            arrival_searches=[
                postcodes.ArrivalSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=arrival_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
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

    if arrival_time is not None and departure_time is not None:
        raise ApiError('arrival_time and departure_time cannot be both specified')

    if arrival_time is not None:
        return DistrictsRequest(
            arrival_searches=[
                zones.ArrivalSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=arrival_time,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[]
        )
    elif departure_time is not None:
        return DistrictsRequest(
            arrival_searches=[
                zones.ArrivalSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=departure_time,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
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

    if arrival_time is not None and departure_time is not None:
        raise ApiError('arrival_time and departure_time cannot be both specified')

    if arrival_time is not None:
        return SectorsRequest(
            arrival_searches=[
                zones.ArrivalSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=arrival_time,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[]
        )
    elif departure_time is not None:
        return SectorsRequest(
            departure_searches=[
                zones.DepartureSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=departure_time,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')


def create_time_map(
    coordinates: List[Coordinates],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    travel_time: int,
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    search_range: Optional[Range]
) -> TimeMapRequest:
    if arrival_time is not None and departure_time is not None:
        raise ApiError('arrival_time and departure_time cannot be both specified')

    if arrival_time is not None:
        return TimeMapRequest(
            arrival_searches=[
                time_map.ArrivalSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=arrival_time,
                    transportation=transportation,
                    range=search_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[],
            intersections=[]
        )
    elif departure_time is not None:
        return TimeMapRequest(
            departure_searches=[
                time_map.DepartureSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=departure_time,
                    transportation=transportation,
                    range=search_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[],
            intersections=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')


def create_intersection(
    coordinates: List[Coordinates],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    travel_time: int,
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    search_range: Optional[Range]
) -> TimeMapRequest:
    if arrival_time is not None and departure_time is not None:
        raise ApiError('arrival_time and departure_time cannot be both specified')

    if arrival_time is not None:
        return TimeMapRequest(
            arrival_searches=[
                time_map.ArrivalSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=arrival_time,
                    transportation=transportation,
                    range=search_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[],
            intersections=[
                time_map.Intersection(
                    id='Intersection search',
                    search_ids=[f'Search {ind}' for ind, _ in enumerate(coordinates)]
                )
            ]
        )
    elif departure_time is not None:
        return TimeMapRequest(
            departure_searches=[
                time_map.DepartureSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=departure_time,
                    transportation=transportation,
                    range=search_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[],
            intersections=[
                time_map.Intersection(
                    id='Intersection search',
                    search_ids=[f'Search {ind}' for ind, _ in enumerate(coordinates)]
                )
            ]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')


def create_union(
    coordinates: List[Coordinates],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    travel_time: int,
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    search_range: Optional[Range]
) -> TimeMapRequest:
    if arrival_time is not None and departure_time is not None:
        raise ApiError('arrival_time and departure_time cannot be both specified')

    if arrival_time is not None:
        return TimeMapRequest(
            arrival_searches=[
                time_map.ArrivalSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=arrival_time,
                    transportation=transportation,
                    range=search_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[
                time_map.Union(
                    id='Union search',
                    search_ids=[f'Search {ind}' for ind, _ in enumerate(coordinates)]
                )
            ],
            intersections=[]
        )
    elif departure_time is not None:
        return TimeMapRequest(
            departure_searches=[
                time_map.DepartureSearch(
                    id=f'Search {ind}',
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=departure_time,
                    transportation=transportation,
                    range=search_range
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[
                time_map.Union(
                    id='Union search',
                    search_ids=[f'Search {ind}' for ind, _ in enumerate(coordinates)]
                )
            ],
            intersections=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')


def create_routes(
    locations: List[Location],
    search_ids: Dict[str, List[str]],
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
    departure_time: Optional[datetime],
    arrival_time: Optional[datetime],
    properties: Optional[List[Property]],
    full_range: Optional[FullRange]
) -> RoutesRequest:
    if arrival_time is not None and departure_time is not None:
        raise ApiError('arrival_time and departure_time cannot be both specified')

    if properties is None:
        properties = [Property.TRAVEL_TIME]
    if arrival_time is not None:
        return RoutesRequest(
            locations=locations,
            arrival_searches=[
                routes.ArrivalSearch(
                    id=arrival_id,
                    arrival_location_id=arrival_id,
                    departure_location_ids=[departure_id for departure_id in departure_ids],
                    arrival_time=arrival_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for arrival_id, departure_ids in search_ids.items()
            ],
            departure_searches=[]
        )
    elif departure_time is not None:
        return RoutesRequest(
            locations=locations,
            departure_searches=[
                routes.DepartureSearch(
                    id=departure_id,
                    departure_location_id=departure_id,
                    arrival_location_ids=[arrival_id for arrival_id in arrival_ids],
                    departure_time=departure_time,
                    transportation=transportation,
                    properties=properties,
                    full_range=full_range
                )
                for departure_id, arrival_ids in search_ids.items()
            ],
            arrival_searches=[]
        )
    else:
        raise ApiError('arrival_time or departure_time should be specified')


def create_proto_request(
    origin: Coordinates,
    destinations: List[Coordinates],
    transportation: ProtoTransportation,
    travel_time: int
) -> TimeFilterFastRequest_pb2.TimeFilterFastRequest:
    request = TimeFilterFastRequest_pb2.TimeFilterFastRequest()

    request.oneToManyRequest.departureLocation.lat = origin.lat
    request.oneToManyRequest.departureLocation.lng = origin.lng

    request.oneToManyRequest.transportation.type = transportation.value.code
    request.oneToManyRequest.travelTime = travel_time
    request.oneToManyRequest.arrivalTimePeriod = TimeFilterFastRequest_pb2.TimePeriod.WEEKDAY_MORNING

    mult = math.pow(10, 5)
    for destination in destinations:
        lat_delta = round((destination.lat - origin.lat) * mult)
        lng_delta = round((destination.lng - origin.lng) * mult)
        request.oneToManyRequest.locationDeltas.extend([lat_delta, lng_delta])

    return request
