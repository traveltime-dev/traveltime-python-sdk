from shapely import wkt, GEOSException
from shapely.geometry import (
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
)

from traveltimepy import Coordinates
from traveltimepy.dto.responses.wkt_response_wrapper.src import (
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
)

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

SUPPORTED_GEOMETRY_TYPES = [
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
]


def parse_point(geometry):
    coords = Coordinates(lat=geometry.coords[0][0], lng=geometry.coords[0][1])
    return PointModel(type=GeometryType.POINT, coordinates=coords)


def parse_line_string(geometry):
    coords = LineStringCoordinates(
        coords=[Coordinates(lat=lat, lng=lng) for lat, lng in geometry.coords]
    )
    return LineStringModel(type=GeometryType.LINESTRING, coordinates=coords)


def parse_polygon(geometry):
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


def parse_multi_point(geometry):
    coords = MultiPointCoordinates(
        points=[Coordinates(lat=point.x, lng=point.y) for point in geometry.geoms]
    )
    return MultiPointModel(type=GeometryType.MULTIPOINT, coordinates=coords)


def parse_multi_line_string(geometry):
    coords = MultiLineStringCoordinates(
        lines=[
            LineStringCoordinates(
                coords=[Coordinates(lat=lat, lng=lng) for lat, lng in line.coords]
            )
            for line in geometry.geoms
        ]
    )
    return MultiLineStringModel(type=GeometryType.MULTILINESTRING, coordinates=coords)


def parse_multi_polygon(geometry):
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


def parse_wkt(wkt_str):
    try:
        geometry = wkt.loads(wkt_str)
    except GEOSException:
        raise InvalidWKTStringError(wkt_str)

    if geometry is None:
        raise NullGeometryError()

    if type(geometry) not in SUPPORTED_GEOMETRY_TYPES:
        raise InvalidGeometryTypeError(geometry)

    type_to_function = {
        Point: parse_point,
        LineString: parse_line_string,
        Polygon: parse_polygon,
        MultiPoint: parse_multi_point,
        MultiLineString: parse_multi_line_string,
        MultiPolygon: parse_multi_polygon,
    }

    func = type_to_function.get(type(geometry))

    if func is None:
        raise InvalidFunctionError(geometry)

    return func(geometry)
