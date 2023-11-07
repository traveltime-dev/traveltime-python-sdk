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

from wkt.src.coordinates_models import (
    LineStringCoordinates,
    PolygonCoordinates,
    MultiPointCoordinates,
    MultiLineStringCoordinates,
    MultiPolygonCoordinates,
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
def _parse_point(geometry: Point):
    coords = Coordinates(lat=geometry.coords[0][0], lng=geometry.coords[0][1])
    return PointModel(type=GeometryType.POINT, coordinates=coords)


@_parse_geometry.register
def _parse_line_string(geometry: LineString):
    coords = LineStringCoordinates(
        coords=[Coordinates(lat=lat, lng=lng) for lat, lng in geometry.coords]
    )
    return LineStringModel(type=GeometryType.LINESTRING, coordinates=coords)


@_parse_geometry.register
def _parse_polygon(geometry: Polygon):
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


@_parse_geometry.register
def _parse_multi_point(geometry: MultiPoint):
    coords = MultiPointCoordinates(
        points=[Coordinates(lat=point.x, lng=point.y) for point in geometry.geoms]
    )
    return MultiPointModel(type=GeometryType.MULTIPOINT, coordinates=coords)


@_parse_geometry.register
def _parse_multi_line_string(geometry: MultiLineString):
    coords = MultiLineStringCoordinates(
        lines=[
            LineStringCoordinates(
                coords=[Coordinates(lat=lat, lng=lng) for lat, lng in line.coords]
            )
            for line in geometry.geoms
        ]
    )
    return MultiLineStringModel(type=GeometryType.MULTILINESTRING, coordinates=coords)


@_parse_geometry.register
def _parse_multi_polygon(geometry: MultiPolygon) -> MultiPolygonModel:
    polygons = (
        PolygonCoordinates(
            exterior=[
                Coordinates(lat=lat, lng=lng) for lat, lng in polygon.exterior.coords
            ],
            interiors=[
                [Coordinates(lat=lat, lng=lng) for lat, lng in interior.coords]
                for interior in polygon.interiors
            ],
        )
        for polygon in geometry.geoms
    )
    coords = MultiPolygonCoordinates(polygons=list(polygons))
    return MultiPolygonModel(type=GeometryType.MULTIPOLYGON, coordinates=coords)


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
