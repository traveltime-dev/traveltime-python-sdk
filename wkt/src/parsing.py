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

from traveltimepy import Coordinates
from wkt.src import (
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
)
from wkt.src.constants import (
    SUPPORTED_GEOMETRY_TYPES,
)

from wkt.src.error import (
    InvalidWKTStringError,
    NullGeometryError,
    InvalidFunctionError,
    InvalidGeometryTypeError,
)
from wkt.src.geometries import GeometryType


def _check_empty(geometry):
    if geometry.is_empty or geometry is None:
        raise NullGeometryError()


@singledispatch
def _parse_geometry(geometry: BaseGeometry):
    raise InvalidFunctionError(geometry)


@_parse_geometry.register
def _parse_point(geometry: Point) -> PointModel:
    return PointModel(
        type=GeometryType.POINT, coordinates=Coordinates(lat=geometry.y, lng=geometry.x)
    )


@_parse_geometry.register
def _parse_line_string(geometry: LineString) -> LineStringModel:
    point_models = [
        PointModel(type=GeometryType.POINT, coordinates=Coordinates(lat=lat, lng=lng))
        for lat, lng in geometry.coords
    ]
    return LineStringModel(type=GeometryType.LINESTRING, coordinates=point_models)


@_parse_geometry.register
def _parse_polygon(geometry: Polygon) -> PolygonModel:
    exterior_points = [
        PointModel(type=GeometryType.POINT, coordinates=Coordinates(lat=lat, lng=lng))
        for lat, lng in geometry.exterior.coords
    ]
    interiors_points = [
        [
            PointModel(
                type=GeometryType.POINT, coordinates=Coordinates(lat=lat, lng=lng)
            )
            for lat, lng in interior.coords
        ]
        for interior in geometry.interiors
    ]
    exterior_line = LineStringModel(
        type=GeometryType.LINESTRING, coordinates=exterior_points
    )
    interior_lines = [
        LineStringModel(type=GeometryType.LINESTRING, coordinates=points)
        for points in interiors_points
    ]
    return PolygonModel(
        type=GeometryType.POLYGON, exterior=exterior_line, interiors=interior_lines
    )


@_parse_geometry.register
def _parse_multi_point(geometry: MultiPoint) -> MultiPointModel:
    point_models = [
        PointModel(
            type=GeometryType.POINT, coordinates=Coordinates(lat=point.y, lng=point.x)
        )
        for point in geometry.geoms
    ]
    return MultiPointModel(type=GeometryType.MULTIPOINT, coordinates=point_models)


@_parse_geometry.register
def _parse_multi_line_string(geometry: MultiLineString) -> MultiLineStringModel:
    line_strings = [
        LineStringModel(
            type=GeometryType.LINESTRING,
            coordinates=[
                PointModel(
                    type=GeometryType.POINT,
                    coordinates=Coordinates(lat=point[0], lng=point[1]),
                )
                for point in linestring.coords
            ],
        )
        for linestring in geometry.geoms
    ]
    return MultiLineStringModel(
        type=GeometryType.MULTILINESTRING, coordinates=line_strings
    )


@_parse_geometry.register
def _parse_multi_polygon(geometry: MultiPolygon) -> MultiPolygonModel:
    polygons = [
        PolygonModel(
            type=GeometryType.POLYGON,
            exterior=LineStringModel(
                type=GeometryType.LINESTRING,
                coordinates=[
                    PointModel(
                        type=GeometryType.POINT,
                        coordinates=Coordinates(lat=point[0], lng=point[1]),
                    )
                    for point in polygon.exterior.coords
                ],
            ),
            interiors=[
                LineStringModel(
                    type=GeometryType.LINESTRING,
                    coordinates=[
                        PointModel(
                            type=GeometryType.POINT,
                            coordinates=Coordinates(lat=point[0], lng=point[1]),
                        )
                        for point in interior.coords
                    ],
                )
                for interior in polygon.interiors
            ],
        )
        for polygon in geometry.geoms
    ]
    return MultiPolygonModel(type=GeometryType.MULTIPOLYGON, coordinates=polygons)


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
