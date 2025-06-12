from functools import singledispatch
from typing import Union

from shapely import wkt, GEOSException
from shapely.geometry import (
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
)
from shapely.geometry.base import BaseGeometry

from traveltimepy.requests.common import Coordinates
from traveltimepy.wkt.geometries import (
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
)
from traveltimepy.wkt.constants import (
    SUPPORTED_GEOMETRY_TYPES,
)

from traveltimepy.wkt.error import (
    InvalidWKTStringError,
    NullGeometryError,
    InvalidFunctionError,
    InvalidGeometryTypeError,
)


def _check_empty(geometry):
    if geometry.is_empty or geometry is None:
        raise NullGeometryError()


@singledispatch
def _parse_geometry(geometry: BaseGeometry):
    raise InvalidFunctionError(geometry)


@_parse_geometry.register
def _parse_point(geometry: Point) -> PointModel:
    return PointModel(coordinates=Coordinates(lat=geometry.y, lng=geometry.x))


@_parse_geometry.register
def _parse_line_string(geometry: LineString) -> LineStringModel:
    point_models = [
        PointModel(coordinates=Coordinates(lat=lat, lng=lng))
        for lat, lng in geometry.coords
    ]
    return LineStringModel(coordinates=point_models)


@_parse_geometry.register
def _parse_polygon(geometry: Polygon) -> PolygonModel:
    exterior_points = [
        PointModel(coordinates=Coordinates(lat=lat, lng=lng))
        for lat, lng in geometry.exterior.coords
    ]
    interiors_points = [
        [
            PointModel(coordinates=Coordinates(lat=lat, lng=lng))
            for lat, lng in interior.coords
        ]
        for interior in list(geometry.interiors)
    ]
    exterior_line = LineStringModel(coordinates=exterior_points)
    interior_lines = [
        LineStringModel(coordinates=points) for points in interiors_points
    ]
    return PolygonModel(exterior=exterior_line, interiors=interior_lines)


@_parse_geometry.register
def _parse_multi_point(geometry: MultiPoint) -> MultiPointModel:
    point_models = [
        PointModel(coordinates=Coordinates(lat=point.y, lng=point.x))
        for point in geometry.geoms
    ]
    return MultiPointModel(coordinates=point_models)


@_parse_geometry.register
def _parse_multi_line_string(geometry: MultiLineString) -> MultiLineStringModel:
    line_strings = [
        LineStringModel(
            coordinates=[
                PointModel(
                    coordinates=Coordinates(lat=point[0], lng=point[1]),
                )
                for point in linestring.coords
            ],
        )
        for linestring in geometry.geoms
    ]
    return MultiLineStringModel(coordinates=line_strings)


@_parse_geometry.register
def _parse_multi_polygon(geometry: MultiPolygon) -> MultiPolygonModel:
    polygons = [
        PolygonModel(
            exterior=LineStringModel(
                coordinates=[
                    PointModel(
                        coordinates=Coordinates(lat=point[0], lng=point[1]),
                    )
                    for point in polygon.exterior.coords
                ],
            ),
            interiors=[
                LineStringModel(
                    coordinates=[
                        PointModel(
                            coordinates=Coordinates(lat=point[0], lng=point[1]),
                        )
                        for point in interior.coords
                    ],
                )
                for interior in list(polygon.interiors)
            ],
        )
        for polygon in geometry.geoms
    ]
    return MultiPolygonModel(coordinates=polygons)


def parse_wkt(
    wkt_str: str,
) -> Union[
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
]:
    try:
        geometry = wkt.loads(wkt_str)
    except GEOSException:
        raise InvalidWKTStringError(wkt_str)

    _check_empty(geometry)

    if type(geometry) not in SUPPORTED_GEOMETRY_TYPES:
        raise InvalidGeometryTypeError(geometry)

    return _parse_geometry(geometry)
