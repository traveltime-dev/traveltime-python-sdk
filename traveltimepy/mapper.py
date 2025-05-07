import math
from typing import Dict, Union, List, Optional

from traveltimepy.dto.requests import time_map_fast
from traveltimepy.dto.requests import h3
from traveltimepy.dto.requests import geohash
from traveltimepy.dto.requests import h3_fast
from traveltimepy.dto.requests import geohash_fast
from traveltimepy.dto.requests.distance_map import DistanceMapRequest
from traveltimepy.dto.requests.geohash import GeohashRequest
from traveltimepy.dto.requests.h3 import H3Request
from traveltimepy.dto.requests.time_map_geojson import TimeMapRequestGeojson
from traveltimepy.dto.requests.time_map_wkt import TimeMapWKTRequest
from traveltimepy.errors import ApiError
import TimeFilterFastRequest_pb2  # type: ignore
import RequestsCommon_pb2  # type: ignore

from traveltimepy.dto.common import (
    CellProperty,
    GeohashCentroid,
    H3Centroid,
    Location,
    Coordinates,
    FullRange,
    PolygonsFilter,
    Property,
    Range,
    LevelOfDetail,
    PropertyProto,
    RenderMode,
    TimeInfo,
    ArrivalTime,
    DepartureTime,
    Snapping,
)
from traveltimepy.dto.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)
from traveltimepy.dto.requests.time_filter_fast import Transportation
from traveltimepy.dto.requests.postcodes_zones import ZonesProperty

from traveltimepy.dto.requests.postcodes import PostcodesRequest
from traveltimepy.dto.requests.routes import RoutesRequest
from traveltimepy.dto.requests.time_filter import TimeFilterRequest
from traveltimepy.dto.requests.time_filter_fast import TimeFilterFastRequest
from traveltimepy.dto.requests.time_map_fast import TimeMapFastRequest
from traveltimepy.dto.requests.time_map_fast_geojson import TimeMapFastGeojsonRequest
from traveltimepy.dto.requests.time_map_fast_wkt import TimeMapFastWKTRequest
from traveltimepy.dto.requests.time_filter_proto import (
    DrivingAndPublicTransportWithDetails,
    ProtoTransportation,
    PublicTransportWithDetails,
)
from traveltimepy.dto.requests.h3_fast import H3FastRequest
from traveltimepy.dto.requests.geohash_fast import GeohashFastRequest
from traveltimepy.dto.requests.postcodes_zones import (
    PostcodesDistrictsRequest,
    PostcodesSectorsRequest,
)
from traveltimepy.dto.requests.time_map import TimeMapRequest

from traveltimepy.dto.requests import (
    distance_map,
    time_filter,
    time_filter_fast,
    postcodes,
    postcodes_zones,
    routes,
    time_map,
)


def create_time_filter(
    locations: List[Location],
    search_ids: Dict[str, List[str]],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    properties: Optional[List[Property]],
    time_info: TimeInfo,
    travel_time: int,
    range: Optional[FullRange],
    snapping: Optional[Snapping],
) -> TimeFilterRequest:
    if properties is None:
        properties = [Property.TRAVEL_TIME]
    if isinstance(time_info, ArrivalTime):
        return TimeFilterRequest(
            locations=locations,
            arrival_searches=[
                time_filter.ArrivalSearch(
                    id=arrival_id,
                    arrival_location_id=arrival_id,
                    departure_location_ids=[
                        departure_id for departure_id in departure_ids
                    ],
                    arrival_time=time_info.value,
                    travel_time=travel_time,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                    snapping=snapping,
                )
                for arrival_id, departure_ids in search_ids.items()
            ],
            departure_searches=[],
        )
    elif isinstance(time_info, DepartureTime):
        return TimeFilterRequest(
            locations=locations,
            departure_searches=[
                time_filter.DepartureSearch(
                    id=departure_id,
                    departure_location_id=departure_id,
                    arrival_location_ids=[arrival_id for arrival_id in arrival_ids],
                    departure_time=time_info.value,
                    travel_time=travel_time,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                    snapping=snapping,
                )
                for departure_id, arrival_ids in search_ids.items()
            ],
            arrival_searches=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_time_map_fast(
    coordinates: List[Coordinates],
    transportation: time_map_fast.Transportation,
    travel_time: int,
    level_of_detail: Optional[LevelOfDetail],
    snapping: Optional[Snapping],
    polygons_filter: Optional[PolygonsFilter],
    render_mode: Optional[RenderMode],
    one_to_many: bool,
) -> TimeMapFastRequest:
    if one_to_many:
        return TimeMapFastRequest(
            arrival_searches=time_map_fast.ArrivalSearches(
                one_to_many=[
                    time_map_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        level_of_detail=level_of_detail,
                        snapping=snapping,
                        polygons_filter=polygons_filter,
                        render_mode=render_mode,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                many_to_one=[],
            ),
        )
    else:
        return TimeMapFastRequest(
            arrival_searches=time_map_fast.ArrivalSearches(
                many_to_one=[
                    time_map_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        level_of_detail=level_of_detail,
                        snapping=snapping,
                        polygons_filter=polygons_filter,
                        render_mode=render_mode,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                one_to_many=[],
            ),
        )


def create_time_map_fast_geojson(
    coordinates: List[Coordinates],
    transportation: time_map_fast.Transportation,
    travel_time: int,
    level_of_detail: Optional[LevelOfDetail],
    snapping: Optional[Snapping],
    polygons_filter: Optional[PolygonsFilter],
    render_mode: Optional[RenderMode],
    one_to_many: bool,
) -> TimeMapFastGeojsonRequest:
    if one_to_many:
        return TimeMapFastGeojsonRequest(
            arrival_searches=time_map_fast.ArrivalSearches(
                one_to_many=[
                    time_map_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        level_of_detail=level_of_detail,
                        snapping=snapping,
                        polygons_filter=polygons_filter,
                        render_mode=render_mode,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                many_to_one=[],
            ),
        )
    else:
        return TimeMapFastGeojsonRequest(
            arrival_searches=time_map_fast.ArrivalSearches(
                many_to_one=[
                    time_map_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        level_of_detail=level_of_detail,
                        snapping=snapping,
                        polygons_filter=polygons_filter,
                        render_mode=render_mode,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                one_to_many=[],
            ),
        )


def create_time_map_fast_wkt(
    coordinates: List[Coordinates],
    transportation: time_map_fast.Transportation,
    travel_time: int,
    level_of_detail: Optional[LevelOfDetail],
    snapping: Optional[Snapping],
    polygons_filter: Optional[PolygonsFilter],
    render_mode: Optional[RenderMode],
    one_to_many: bool,
) -> TimeMapFastWKTRequest:
    if one_to_many:
        return TimeMapFastWKTRequest(
            arrival_searches=time_map_fast.ArrivalSearches(
                one_to_many=[
                    time_map_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        level_of_detail=level_of_detail,
                        snapping=snapping,
                        polygons_filter=polygons_filter,
                        render_mode=render_mode,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                many_to_one=[],
            ),
        )
    else:
        return TimeMapFastWKTRequest(
            arrival_searches=time_map_fast.ArrivalSearches(
                many_to_one=[
                    time_map_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        level_of_detail=level_of_detail,
                        snapping=snapping,
                        polygons_filter=polygons_filter,
                        render_mode=render_mode,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                one_to_many=[],
            ),
        )


def create_h3_fast(
    coordinates: List[Union[Coordinates, H3Centroid]],
    properties: List[CellProperty],
    resolution: int,
    transportation: h3_fast.Transportation,
    travel_time: int,
    snapping: Optional[Snapping],
    one_to_many: bool,
) -> H3FastRequest:
    if one_to_many:
        return H3FastRequest(
            resolution=resolution,
            properties=properties,
            arrival_searches=h3_fast.ArrivalSearches(
                one_to_many=[
                    h3_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        snapping=snapping,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                many_to_one=[],
            ),
        )
    else:
        return H3FastRequest(
            resolution=resolution,
            properties=properties,
            arrival_searches=h3_fast.ArrivalSearches(
                many_to_one=[
                    h3_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        snapping=snapping,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                one_to_many=[],
            ),
        )


def create_geohash_fast(
    coordinates: List[Union[Coordinates, GeohashCentroid]],
    properties: List[CellProperty],
    resolution: int,
    transportation: geohash_fast.Transportation,
    travel_time: int,
    snapping: Optional[Snapping],
    one_to_many: bool,
) -> GeohashFastRequest:
    if one_to_many:
        return GeohashFastRequest(
            resolution=resolution,
            properties=properties,
            arrival_searches=geohash_fast.ArrivalSearches(
                one_to_many=[
                    geohash_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        snapping=snapping,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                many_to_one=[],
            ),
        )
    else:
        return GeohashFastRequest(
            resolution=resolution,
            properties=properties,
            arrival_searches=geohash_fast.ArrivalSearches(
                many_to_one=[
                    geohash_fast.Search(
                        id=f"Search {ind}",
                        coords=cur_coordinates,
                        transportation=transportation,
                        travel_time=travel_time,
                        arrival_time_period="weekday_morning",
                        snapping=snapping,
                    )
                    for ind, cur_coordinates in enumerate(coordinates)
                ],
                one_to_many=[],
            ),
        )


def create_time_filter_fast(
    locations: List[Location],
    search_ids: Dict[str, List[str]],
    transportation: Transportation,
    travel_time: int,
    properties: Optional[List[Property]],
    one_to_many: bool,
    snapping: Optional[Snapping],
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
                        arrival_time_period="weekday_morning",
                        properties=properties,
                        snapping=snapping,
                    )
                    for departure_id, arrival_ids in search_ids.items()
                ],
                many_to_one=[],
            ),
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
                        arrival_time_period="weekday_morning",
                        properties=properties,
                        snapping=snapping,
                    )
                    for arrival_id, departure_ids in search_ids.items()
                ],
                one_to_many=[],
            ),
        )


def create_postcodes(
    coordinates: List[Coordinates],
    time_info: TimeInfo,
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    travel_time: int,
    properties: Optional[List[Property]],
    range: Optional[FullRange],
) -> PostcodesRequest:
    if properties is None:
        properties = [Property.TRAVEL_TIME]

    if isinstance(time_info, DepartureTime):
        return PostcodesRequest(
            departure_searches=[
                postcodes.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
        )
    elif isinstance(time_info, ArrivalTime):
        return PostcodesRequest(
            arrival_searches=[
                postcodes.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_districts(
    coordinates: List[Coordinates],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    travel_time: int,
    time_info: TimeInfo,
    reachable_postcodes_threshold,
    properties: Optional[List[ZonesProperty]],
    range: Optional[FullRange],
) -> PostcodesDistrictsRequest:
    if properties is None:
        properties = [ZonesProperty.TRAVEL_TIME_ALL]

    if isinstance(time_info, ArrivalTime):
        return PostcodesDistrictsRequest(
            arrival_searches=[
                postcodes_zones.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
        )
    elif isinstance(time_info, DepartureTime):
        return PostcodesDistrictsRequest(
            departure_searches=[
                postcodes_zones.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_sectors(
    coordinates: List[Coordinates],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    travel_time: int,
    time_info: TimeInfo,
    reachable_postcodes_threshold,
    properties: Optional[List[ZonesProperty]],
    range: Optional[FullRange],
) -> PostcodesSectorsRequest:
    if properties is None:
        properties = [ZonesProperty.TRAVEL_TIME_ALL]

    if isinstance(time_info, ArrivalTime):
        return PostcodesSectorsRequest(
            arrival_searches=[
                postcodes_zones.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
        )
    elif isinstance(time_info, DepartureTime):
        return PostcodesSectorsRequest(
            departure_searches=[
                postcodes_zones.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    reachable_postcodes_threshold=reachable_postcodes_threshold,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_time_map(
    coordinates: List[Coordinates],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    travel_time: int,
    time_info: TimeInfo,
    search_range: Optional[Range],
    level_of_detail: Optional[LevelOfDetail],
    snapping: Optional[Snapping],
    polygons_filter: Optional[PolygonsFilter],
    remove_water_bodies: Optional[bool],
    render_mode: Optional[RenderMode],
) -> TimeMapRequest:
    if isinstance(time_info, ArrivalTime):
        return TimeMapRequest(
            arrival_searches=[
                time_map.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[],
            intersections=[],
        )
    elif isinstance(time_info, DepartureTime):
        return TimeMapRequest(
            departure_searches=[
                time_map.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[],
            intersections=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_time_map_geojson(
    coordinates: List[Coordinates],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    travel_time: int,
    time_info: TimeInfo,
    search_range: Optional[Range],
    level_of_detail: Optional[LevelOfDetail],
    snapping: Optional[Snapping],
    polygons_filter: Optional[PolygonsFilter],
    remove_water_bodies: Optional[bool],
    render_mode: Optional[RenderMode],
) -> TimeMapRequestGeojson:
    if isinstance(time_info, ArrivalTime):
        return TimeMapRequestGeojson(
            arrival_searches=[
                time_map.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
        )
    elif isinstance(time_info, DepartureTime):
        return TimeMapRequestGeojson(
            departure_searches=[
                time_map.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_time_map_wkt(
    coordinates: List[Coordinates],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    travel_time: int,
    time_info: TimeInfo,
    search_range: Optional[Range],
    level_of_detail: Optional[LevelOfDetail],
    snapping: Optional[Snapping],
    polygons_filter: Optional[PolygonsFilter],
    remove_water_bodies: Optional[bool],
    render_mode: Optional[RenderMode],
) -> TimeMapWKTRequest:
    if isinstance(time_info, ArrivalTime):
        return TimeMapWKTRequest(
            arrival_searches=[
                time_map.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
        )
    elif isinstance(time_info, DepartureTime):
        return TimeMapWKTRequest(
            departure_searches=[
                time_map.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    level_of_detail=level_of_detail,
                    range=search_range,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_h3(
    coordinates: List[Union[Coordinates, H3Centroid]],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    resolution: int,
    travel_time: int,
    properties: List[CellProperty],
    time_info: TimeInfo,
    search_range: Optional[Range],
    snapping: Optional[Snapping],
) -> H3Request:
    if isinstance(time_info, ArrivalTime):
        return H3Request(
            resolution=resolution,
            properties=properties,
            arrival_searches=[
                h3.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[],
            intersections=[],
        )
    elif isinstance(time_info, DepartureTime):
        return H3Request(
            resolution=resolution,
            properties=properties,
            departure_searches=[
                h3.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[],
            intersections=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_geohash(
    coordinates: List[Union[Coordinates, GeohashCentroid]],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    resolution: int,
    travel_time: int,
    properties: List[CellProperty],
    time_info: TimeInfo,
    search_range: Optional[Range],
    snapping: Optional[Snapping],
) -> GeohashRequest:
    if isinstance(time_info, ArrivalTime):
        return GeohashRequest(
            resolution=resolution,
            properties=properties,
            arrival_searches=[
                geohash.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[],
            intersections=[],
        )
    elif isinstance(time_info, DepartureTime):
        return GeohashRequest(
            resolution=resolution,
            properties=properties,
            departure_searches=[
                geohash.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[],
            intersections=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_distance_map(
    coordinates: List[Coordinates],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    travel_distance: int,
    time_info: TimeInfo,
    level_of_detail: Optional[LevelOfDetail],
    snapping: Optional[Snapping],
    polygons_filter: Optional[PolygonsFilter],
    no_holes: Optional[bool],
) -> DistanceMapRequest:
    if isinstance(time_info, ArrivalTime):
        return DistanceMapRequest(
            arrival_searches=[
                distance_map.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_distance=travel_distance,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    no_holes=no_holes,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[],
            intersections=[],
        )
    elif isinstance(time_info, DepartureTime):
        return DistanceMapRequest(
            departure_searches=[
                distance_map.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_distance=travel_distance,
                    departure_time=time_info.value,
                    transportation=transportation,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    no_holes=no_holes,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[],
            intersections=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_time_map_intersection(
    coordinates: List[Coordinates],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    travel_time: int,
    time_info: TimeInfo,
    search_range: Optional[Range],
    level_of_detail: Optional[LevelOfDetail],
    snapping: Optional[Snapping],
    polygons_filter: Optional[PolygonsFilter],
    remove_water_bodies: Optional[bool],
    render_mode: Optional[RenderMode],
) -> TimeMapRequest:
    if isinstance(time_info, ArrivalTime):
        return TimeMapRequest(
            arrival_searches=[
                time_map.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[],
            intersections=[
                time_map.Intersection(
                    id="Intersection search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
        )
    elif isinstance(time_info, DepartureTime):
        return TimeMapRequest(
            departure_searches=[
                time_map.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[],
            intersections=[
                time_map.Intersection(
                    id="Intersection search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_h3_intersection(
    coordinates: List[Union[Coordinates, H3Centroid]],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    resolution: int,
    travel_time: int,
    properties: List[CellProperty],
    time_info: TimeInfo,
    search_range: Optional[Range],
    snapping: Optional[Snapping],
) -> H3Request:
    if isinstance(time_info, ArrivalTime):
        return H3Request(
            resolution=resolution,
            properties=properties,
            arrival_searches=[
                h3.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[],
            intersections=[
                h3.Intersection(
                    id="Intersection search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
        )
    elif isinstance(time_info, DepartureTime):
        return H3Request(
            resolution=resolution,
            properties=properties,
            departure_searches=[
                h3.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[],
            intersections=[
                h3.Intersection(
                    id="Intersection search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_geohash_intersection(
    coordinates: List[Union[Coordinates, GeohashCentroid]],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    resolution: int,
    travel_time: int,
    properties: List[CellProperty],
    time_info: TimeInfo,
    search_range: Optional[Range],
    snapping: Optional[Snapping],
) -> GeohashRequest:
    if isinstance(time_info, ArrivalTime):
        return GeohashRequest(
            resolution=resolution,
            properties=properties,
            arrival_searches=[
                geohash.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[],
            intersections=[
                geohash.Intersection(
                    id="Intersection search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
        )
    elif isinstance(time_info, DepartureTime):
        return GeohashRequest(
            resolution=resolution,
            properties=properties,
            departure_searches=[
                geohash.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[],
            intersections=[
                geohash.Intersection(
                    id="Intersection search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_time_map_union(
    coordinates: List[Coordinates],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    travel_time: int,
    time_info: TimeInfo,
    search_range: Optional[Range],
    level_of_detail: Optional[LevelOfDetail],
    snapping: Optional[Snapping],
    polygons_filter: Optional[PolygonsFilter],
    remove_water_bodies: Optional[bool],
    render_mode: Optional[RenderMode],
) -> TimeMapRequest:
    if isinstance(time_info, ArrivalTime):
        return TimeMapRequest(
            arrival_searches=[
                time_map.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[
                time_map.Union(
                    id="Union search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
            intersections=[],
        )
    elif isinstance(time_info, DepartureTime):
        return TimeMapRequest(
            departure_searches=[
                time_map.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    level_of_detail=level_of_detail,
                    snapping=snapping,
                    polygons_filter=polygons_filter,
                    remove_water_bodies=remove_water_bodies,
                    render_mode=render_mode,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[
                time_map.Union(
                    id="Union search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
            intersections=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_h3_union(
    coordinates: List[Union[Coordinates, H3Centroid]],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    resolution: int,
    travel_time: int,
    properties: List[CellProperty],
    time_info: TimeInfo,
    search_range: Optional[Range],
    snapping: Optional[Snapping],
) -> H3Request:
    if isinstance(time_info, ArrivalTime):
        return H3Request(
            resolution=resolution,
            properties=properties,
            arrival_searches=[
                h3.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[
                h3.Union(
                    id="Union search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
            intersections=[],
        )
    elif isinstance(time_info, DepartureTime):
        return H3Request(
            resolution=resolution,
            properties=properties,
            departure_searches=[
                h3.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[
                h3.Union(
                    id="Union search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
            intersections=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_geohash_union(
    coordinates: List[Union[Coordinates, GeohashCentroid]],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    resolution: int,
    travel_time: int,
    properties: List[CellProperty],
    time_info: TimeInfo,
    search_range: Optional[Range],
    snapping: Optional[Snapping],
) -> GeohashRequest:
    if isinstance(time_info, ArrivalTime):
        return GeohashRequest(
            resolution=resolution,
            properties=properties,
            arrival_searches=[
                geohash.ArrivalSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    arrival_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            departure_searches=[],
            unions=[
                geohash.Union(
                    id="Union search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
            intersections=[],
        )
    elif isinstance(time_info, DepartureTime):
        return GeohashRequest(
            resolution=resolution,
            properties=properties,
            departure_searches=[
                geohash.DepartureSearch(
                    id=f"Search {ind}",
                    coords=cur_coordinates,
                    travel_time=travel_time,
                    departure_time=time_info.value,
                    transportation=transportation,
                    range=search_range,
                    snapping=snapping,
                )
                for ind, cur_coordinates in enumerate(coordinates)
            ],
            arrival_searches=[],
            unions=[
                geohash.Union(
                    id="Union search",
                    search_ids=[f"Search {ind}" for ind, _ in enumerate(coordinates)],
                )
            ],
            intersections=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_routes(
    locations: List[Location],
    search_ids: Dict[str, List[str]],
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ],
    time_info: TimeInfo,
    properties: Optional[List[Property]],
    range: Optional[FullRange],
    snapping: Optional[Snapping],
) -> RoutesRequest:
    if properties is None:
        properties = [Property.TRAVEL_TIME]
    if isinstance(time_info, ArrivalTime):
        return RoutesRequest(
            locations=locations,
            arrival_searches=[
                routes.ArrivalSearch(
                    id=arrival_id,
                    arrival_location_id=arrival_id,
                    departure_location_ids=[
                        departure_id for departure_id in departure_ids
                    ],
                    arrival_time=time_info.value,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                    snapping=snapping,
                )
                for arrival_id, departure_ids in search_ids.items()
            ],
            departure_searches=[],
        )
    elif isinstance(time_info, DepartureTime):
        return RoutesRequest(
            locations=locations,
            departure_searches=[
                routes.DepartureSearch(
                    id=departure_id,
                    departure_location_id=departure_id,
                    arrival_location_ids=[arrival_id for arrival_id in arrival_ids],
                    departure_time=time_info.value,
                    transportation=transportation,
                    properties=properties,
                    range=range,
                    snapping=snapping,
                )
                for departure_id, arrival_ids in search_ids.items()
            ],
            arrival_searches=[],
        )
    else:
        raise ApiError("arrival_time or departure_time should be specified")


def create_proto_request(
    origin: Coordinates,
    destinations: List[Coordinates],
    transportation: Union[
        ProtoTransportation,
        PublicTransportWithDetails,
        DrivingAndPublicTransportWithDetails,
    ],
    properties: Optional[List[PropertyProto]],
    travel_time: int,
    one_to_many: bool,
) -> TimeFilterFastRequest_pb2.TimeFilterFastRequest:  # type: ignore
    request = TimeFilterFastRequest_pb2.TimeFilterFastRequest()  # type: ignore

    req = request.oneToManyRequest if one_to_many else request.manyToOneRequest

    if one_to_many:
        req.departureLocation.lat = origin.lat
        req.departureLocation.lng = origin.lng
    else:
        req.arrivalLocation.lat = origin.lat
        req.arrivalLocation.lng = origin.lng

    # Set transportation type
    if isinstance(transportation, ProtoTransportation):
        req.transportation.type = transportation.value.code
    else:  # PublicTransportDetails or DrivingAndPublicTransportDetails
        req.transportation.type = transportation.TYPE.value.code

        if isinstance(transportation, PublicTransportWithDetails):
            if transportation.walking_time_to_station is not None:
                req.transportation.publicTransport.walkingTimeToStation = (
                    transportation.walking_time_to_station
                )

        elif isinstance(transportation, DrivingAndPublicTransportWithDetails):
            if transportation.walking_time_to_station is not None:
                req.transportation.drivingAndPublicTransport.walkingTimeToStation = (
                    transportation.walking_time_to_station
                )

            if transportation.driving_time_to_station is not None:
                req.transportation.drivingAndPublicTransport.drivingTimeToStation = (
                    transportation.driving_time_to_station
                )

            if transportation.parking_time is not None:
                req.transportation.drivingAndPublicTransport.parkingTime = (
                    transportation.parking_time
                )

    # Set common parameters
    req.travelTime = travel_time
    req.arrivalTimePeriod = RequestsCommon_pb2.TimePeriod.WEEKDAY_MORNING  # type: ignore

    if properties is not None:
        req.properties.extend(properties)

    # Calculate and add location deltas
    mult = math.pow(10, 5)
    for destination in destinations:
        lat_delta = round((destination.lat - origin.lat) * mult)
        lng_delta = round((destination.lng - origin.lng) * mult)
        req.locationDeltas.extend([lat_delta, lng_delta])

    return request
