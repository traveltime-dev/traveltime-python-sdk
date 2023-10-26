from shapely import wkt
from shapely.geometry import (
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
)

from traveltimepy import Coordinates
from traveltimepy.dto.responses.wkt_wrapper import (
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
)

from traveltimepy.dto.responses.wkt_wrapper.coordinates_models import (
    LineStringCoordinates,
    PolygonCoordinates,
    MultiPointCoordinates,
    MultiLineStringCoordinates,
    MultiPolygonCoordinates,
)


def parse_point(geometry):
    coords = Coordinates(lat=geometry.coords[0][0], lng=geometry.coords[0][1])
    return PointModel(type="Point", coordinates=coords)


def parse_line_string(geometry):
    coords = LineStringCoordinates(
        coords=[Coordinates(lat=x, lng=lng) for x, lng in geometry.coords]
    )
    return LineStringModel(type="LineString", coordinates=coords)


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
    return PolygonModel(type="Polygon", coordinates=exterior)


def parse_multi_point(geometry):
    coords = MultiPointCoordinates(
        points=[Coordinates(lat=point.x, lng=point.y) for point in geometry.geoms]
    )
    return MultiPointModel(type="MultiPoint", coordinates=coords)


def parse_multi_line_string(geometry):
    coords = MultiLineStringCoordinates(
        lines=[
            LineStringCoordinates(
                coords=[Coordinates(lat=lat, lng=lng) for lat, lng in line.coords]
            )
            for line in geometry.geoms
        ]
    )
    return MultiLineStringModel(type="MultiLineString", coordinates=coords)


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
    return MultiPolygonModel(type="MultiPolygon", coordinates=coords)


def parse_wkt(wkt_str):
    geometry = wkt.loads(wkt_str)
    type_to_function = {
        Point: parse_point,
        LineString: parse_line_string,
        Polygon: parse_polygon,
        MultiPoint: parse_multi_point,
        MultiLineString: parse_multi_line_string,
        MultiPolygon: parse_multi_polygon,
    }

    func = type_to_function.get(type(geometry))
    if func:
        return func(geometry)
    else:
        raise ValueError(f"Unsupported geometry: {geometry}")
