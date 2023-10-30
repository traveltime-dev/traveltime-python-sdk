import pytest  # noqa

from traveltimepy import Coordinates
from traveltimepy.dto.responses.wkt_response_wrapper.src import (
    parse_wkt,
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
    InvalidGeometryTypeError,
)
from traveltimepy.dto.responses.wkt_response_wrapper.src.geometries import GeometryType

point_wkt = "POINT (0 0)"
line_wkt = "LINESTRING(0 0, 1 1, 2 2)"
poly_wkt = "POLYGON((0 0, 0 2, 2 2, 2 0, 0 0))"
mp_wkt = "MULTIPOINT(0 0, 1 1)"
mls_wkt = "MULTILINESTRING((0 0, 1 1), (2 2, 3 3))"
mpoly_wkt = "MULTIPOLYGON(((0 0, 0 2, 2 2, 2 0, 0 0)))"


def test_parse_point():
    parsed = parse_wkt(point_wkt)
    assert parsed == PointModel(
        type=GeometryType.POINT, coordinates=Coordinates(lat=0, lng=0)
    )


def test_parse_line_string():
    parsed = parse_wkt(line_wkt)
    assert parsed == LineStringModel(
        type=GeometryType.LINESTRING,
        coordinates=LineStringCoordinates(
            coords=[
                Coordinates(lat=0.0, lng=0.0),
                Coordinates(lat=1.0, lng=1.0),
                Coordinates(lat=2.0, lng=2.0),
            ]
        ),
    )


def test_parse_polygon():
    parsed = parse_wkt(poly_wkt)
    assert parsed == PolygonModel(
        type=GeometryType.POLYGON,
        coordinates=PolygonCoordinates(
            exterior=[
                Coordinates(lat=0.0, lng=0.0),
                Coordinates(lat=0.0, lng=2.0),
                Coordinates(lat=2.0, lng=2.0),
                Coordinates(lat=2.0, lng=0.0),
                Coordinates(lat=0.0, lng=0.0),
            ],
            interiors=[],
        ),
    )


def test_parse_multi_point():
    parsed = parse_wkt(mp_wkt)
    assert parsed == MultiPointModel(
        type=GeometryType.MULTIPOINT,
        coordinates=MultiPointCoordinates(
            points=[Coordinates(lat=0.0, lng=0.0), Coordinates(lat=1.0, lng=1.0)]
        ),
    )


def test_parse_multi_line_string():
    parsed = parse_wkt(mls_wkt)
    assert parsed == MultiLineStringModel(
        type=GeometryType.MULTILINESTRING,
        coordinates=MultiLineStringCoordinates(
            lines=[
                LineStringCoordinates(
                    coords=[
                        Coordinates(lat=0.0, lng=0.0),
                        Coordinates(lat=1.0, lng=1.0),
                    ]
                ),
                LineStringCoordinates(
                    coords=[
                        Coordinates(lat=2.0, lng=2.0),
                        Coordinates(lat=3.0, lng=3.0),
                    ]
                ),
            ]
        ),
    )


def test_parse_multi_polygon():
    parsed = parse_wkt(mpoly_wkt)
    assert parsed == MultiPolygonModel(
        type=GeometryType.MULTIPOLYGON,
        coordinates=MultiPolygonCoordinates(
            polygons=[
                PolygonCoordinates(
                    exterior=[
                        Coordinates(lat=0.0, lng=0.0),
                        Coordinates(lat=0.0, lng=2.0),
                        Coordinates(lat=2.0, lng=2.0),
                        Coordinates(lat=2.0, lng=0.0),
                        Coordinates(lat=0.0, lng=0.0),
                    ],
                    interiors=[],
                )
            ]
        ),
    )


# Invalid WKT string
def test_invalid_wkt_string():
    with pytest.raises(InvalidWKTStringError):
        parse_wkt("INVALIDWKTSTRING")


# Null geometry
def test_null_geometry():
    with pytest.raises(NullGeometryError):
        parse_wkt("POINT EMPTY")


# Unsupported geometry type
def test_unsupported_geometry_type():
    unsupported_wkt = "GEOMETRYCOLLECTION(POINT(2 3),LINESTRING(2 3, 3 4))"
    with pytest.raises(InvalidGeometryTypeError):
        parse_wkt(unsupported_wkt)
