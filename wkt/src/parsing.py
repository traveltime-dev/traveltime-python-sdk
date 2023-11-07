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
    coords = [Coordinates(lat=lat, lng=lng) for lat, lng in geometry.coords]
    return LineStringModel(type=GeometryType.LINESTRING, coordinates=coords)


@_parse_geometry.register
def _parse_polygon(geometry: Polygon) -> PolygonModel:
    exterior_coords = [
        Coordinates(lat=lat, lng=lng) for lat, lng in geometry.exterior.coords
    ]
    interiors_coords = [
        [Coordinates(lat=lat, lng=lng) for lat, lng in interior.coords]
        for interior in geometry.interiors
    ]
    return PolygonModel(
        type=GeometryType.POLYGON,
        exterior=LineStringModel(
            type=GeometryType.LINESTRING, coordinates=exterior_coords
        ),
        interiors=[
            LineStringModel(type=GeometryType.LINESTRING, coordinates=interior)
            for interior in interiors_coords
        ],
    )


@_parse_geometry.register
def _parse_multi_point(geometry: MultiPoint) -> MultiPointModel:
    coords = [
        PointModel(
            type=GeometryType.POINT, coordinates=Coordinates(lat=point.y, lng=point.x)
        )
        for point in geometry.geoms
    ]
    return MultiPointModel(type=GeometryType.MULTIPOINT, coordinates=coords)


@_parse_geometry.register
def _parse_multi_line_string(geometry: MultiLineString) -> MultiLineStringModel:
    coords = [
        LineStringModel(
            type=GeometryType.LINESTRING,
            coordinates=[
                Coordinates(lat=lat, lng=lng) for lat, lng in linestring.coords
            ],
        )
        for linestring in geometry.geoms
    ]
    return MultiLineStringModel(type=GeometryType.MULTILINESTRING, coordinates=coords)


@_parse_geometry.register
def _parse_multi_polygon(geometry: MultiPolygon) -> MultiPolygonModel:
    polygons = [
        PolygonModel(
            type=GeometryType.POLYGON,
            exterior=LineStringModel(
                type=GeometryType.LINESTRING,
                coordinates=[
                    Coordinates(lat=lat, lng=lng)
                    for lat, lng in polygon.exterior.coords
                ],
            ),
            interiors=[
                LineStringModel(
                    type=GeometryType.LINESTRING,
                    coordinates=[
                        Coordinates(lat=lat, lng=lng) for lat, lng in interior.coords
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
