from shapely import wkt
from shapely.geometry import (
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
)

from traveltimepy.dto.responses.wkt_wrapper import (
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
)


def parse_point(geometry):
    return PointModel(type="Point", coordinates=geometry.coords[0])


def parse_line_string(geometry):
    return LineStringModel(type="LineString", coordinates=list(geometry.coords))


def parse_polygon(geometry):
    exterior = list(geometry.exterior.coords)
    interiors = [list(interior.coords) for interior in geometry.interiors]
    return PolygonModel(type="Polygon", coordinates=[exterior] + interiors)


def parse_multi_point(geometry):
    return MultiPointModel(
        type="MultiPoint",
        coordinates=[tuple(coord.coords[0]) for coord in geometry.geoms],
    )


def parse_multi_line_string(geometry):
    return MultiLineStringModel(
        type="MultiLineString",
        coordinates=[list(line.coords) for line in geometry.geoms],
    )


def parse_multi_polygon(geometry):
    multi_polygon_coords = []
    for polygon in geometry.geoms:
        exterior = list(polygon.exterior.coords)
        interiors = [list(interior.coords) for interior in polygon.interiors]
        multi_polygon_coords.append([exterior] + interiors)
    return MultiPolygonModel(type="MultiPolygon", coordinates=multi_polygon_coords)


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
