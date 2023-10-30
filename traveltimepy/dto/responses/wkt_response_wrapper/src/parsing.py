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
from traveltimepy.dto.responses.wkt_response_wrapper.src import (
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
)
from traveltimepy.dto.responses.wkt_response_wrapper.src.constants import SUPPORTED_GEOMETRY_TYPES

from traveltimepy.dto.responses.wkt_response_wrapper.src.coordinates_models import (
    LineStringCoordinates,
    PolygonCoordinates,
    MultiPointCoordinates,
    MultiLineStringCoordinates,
    MultiPolygonCoordinates,
)
from traveltimepy.dto.responses.wkt_response_wrapper.src.error import (
    InvalidWKTStringError,
    NullGeometryError,
    InvalidFunctionError,
    InvalidGeometryTypeError,
)
from traveltimepy.dto.responses.wkt_response_wrapper.src.geometries import GeometryType


def _check_empty(geometry):
    if geometry.is_empty or geometry is None:
        raise NullGeometryError()


def _parse_point(geometry):
    coords = Coordinates(lat=geometry.coords[0][0], lng=geometry.coords[0][1])
    return PointModel(type=GeometryType.POINT, coordinates=coords)


def _parse_line_string(geometry):
    coords = LineStringCoordinates(
        coords=[Coordinates(lat=lat, lng=lng) for lat, lng in geometry.coords]
    )
    return LineStringModel(type=GeometryType.LINESTRING, coordinates=coords)


def _parse_polygon(geometry):
    exterior = PolygonCoordinates(
        exterior=[
            Coordinates(lat=lat, lng=lng) for lat, lng in geometry.exterior.coords
        ],
        interiors=[
            [Coordinates(lat=lat, lng=lng) for lat, lng in interior.coords]
            for interior in geometry.interiors
        ],
    )
    return PolygonModel(type=GeometryType.POLYGON, coordinates=exterior)


def _parse_multi_point(geometry):
    coords = MultiPointCoordinates(
        points=[Coordinates(lat=point.x, lng=point.y) for point in geometry.geoms]
    )
    return MultiPointModel(type=GeometryType.MULTIPOINT, coordinates=coords)


def _parse_multi_line_string(geometry):
    coords = MultiLineStringCoordinates(
        lines=[
            LineStringCoordinates(
                coords=[Coordinates(lat=lat, lng=lng) for lat, lng in line.coords]
            )
            for line in geometry.geoms
        ]
    )
    return MultiLineStringModel(type=GeometryType.MULTILINESTRING, coordinates=coords)


def _parse_multi_polygon(geometry):
    polygons = []
    for polygon in geometry.geoms:
        exterior = [
            Coordinates(lat=lat, lng=lng) for lat, lng in polygon.exterior.coords
        ]
        interiors = [
            [Coordinates(lat=lat, lng=lng) for lat, lng in interior.coords]
            for interior in polygon.interiors
        ]
        polygons.append(PolygonCoordinates(exterior=exterior, interiors=interiors))
    coords = MultiPolygonCoordinates(polygons=polygons)
    return MultiPolygonModel(type=GeometryType.MULTIPOLYGON, coordinates=coords)


@singledispatch
def _parse_geometry(geometry: BaseGeometry):
    raise InvalidFunctionError(geometry)


@_parse_geometry.register
def _(geometry: Point):
    return _parse_point(geometry)


@_parse_geometry.register
def _(geometry: LineString):
    return _parse_line_string(geometry)


@_parse_geometry.register
def _(geometry: Polygon):
    return _parse_polygon(geometry)


@_parse_geometry.register
def _(geometry: MultiPoint):
    return _parse_multi_point(geometry)


@_parse_geometry.register
def _(geometry: MultiLineString):
    return _parse_multi_line_string(geometry)


@_parse_geometry.register
def _(geometry: MultiPolygon):
    return _parse_multi_polygon(geometry)


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
