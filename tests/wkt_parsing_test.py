import pytest  # noqa

from traveltimepy.requests.common import Coordinates
from traveltimepy.wkt import (
    parse_wkt,
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
)
from traveltimepy.wkt.error import (
    InvalidWKTStringError,
    NullGeometryError,
    InvalidGeometryTypeError,
)

point_wkt = "POINT (0 0)"
line_wkt = "LINESTRING(0 0, 1 1, 2 2)"
poly_wkt = "POLYGON((0 0, 0 2, 2 2, 2 0, 0 0))"
mp_wkt = "MULTIPOINT(0 0, 1 1)"
mls_wkt = "MULTILINESTRING((0 0, 1 1), (2 2, 3 3))"
mpoly_wkt = "MULTIPOLYGON(((0 0, 0 2, 2 2, 2 0, 0 0)))"


def test_parse_point():
    parsed = parse_wkt(point_wkt)
    assert parsed == PointModel(coordinates=Coordinates(lat=0, lng=0))


def test_parse_line_string():
    parsed = parse_wkt(line_wkt)
    assert parsed == LineStringModel(
        coordinates=[
            PointModel(coordinates=Coordinates(lat=0.0, lng=0.0)),
            PointModel(coordinates=Coordinates(lat=1.0, lng=1.0)),
            PointModel(coordinates=Coordinates(lat=2.0, lng=2.0)),
        ],
    )


def test_parse_polygon():
    parsed = parse_wkt(poly_wkt)
    assert parsed == PolygonModel(
        exterior=LineStringModel(
            coordinates=[
                PointModel(coordinates=Coordinates(lat=0.0, lng=0.0)),
                PointModel(coordinates=Coordinates(lat=0.0, lng=2.0)),
                PointModel(coordinates=Coordinates(lat=2.0, lng=2.0)),
                PointModel(coordinates=Coordinates(lat=2.0, lng=0.0)),
                PointModel(coordinates=Coordinates(lat=0.0, lng=0.0)),
            ],
        ),
        interiors=[],
    )


def test_parse_multi_point():
    parsed = parse_wkt(mp_wkt)
    assert parsed == MultiPointModel(
        coordinates=[
            PointModel(coordinates=Coordinates(lat=0.0, lng=0.0)),
            PointModel(coordinates=Coordinates(lat=1.0, lng=1.0)),
        ],
    )


def test_parse_multi_line_string():
    parsed = parse_wkt(mls_wkt)
    assert parsed == MultiLineStringModel(
        coordinates=[
            LineStringModel(
                coordinates=[
                    PointModel(
                        coordinates=Coordinates(lat=0.0, lng=0.0),
                    ),
                    PointModel(
                        coordinates=Coordinates(lat=1.0, lng=1.0),
                    ),
                ],
            ),
            LineStringModel(
                coordinates=[
                    PointModel(
                        coordinates=Coordinates(lat=2.0, lng=2.0),
                    ),
                    PointModel(
                        coordinates=Coordinates(lat=3.0, lng=3.0),
                    ),
                ],
            ),
        ],
    )


def test_parse_multi_polygon():
    parsed = parse_wkt(mpoly_wkt)
    assert parsed == MultiPolygonModel(
        coordinates=[
            PolygonModel(
                exterior=LineStringModel(
                    coordinates=[
                        PointModel(
                            coordinates=Coordinates(lat=0.0, lng=0.0),
                        ),
                        PointModel(
                            coordinates=Coordinates(lat=0.0, lng=2.0),
                        ),
                        PointModel(
                            coordinates=Coordinates(lat=2.0, lng=2.0),
                        ),
                        PointModel(
                            coordinates=Coordinates(lat=2.0, lng=0.0),
                        ),
                        PointModel(
                            coordinates=Coordinates(lat=0.0, lng=0.0),
                        ),
                    ],
                ),
                interiors=[],
            )
        ],
    )


def test_invalid_wkt_string():
    with pytest.raises(InvalidWKTStringError):
        parse_wkt("INVALIDWKTSTRING")


def test_null_geometry():
    with pytest.raises(NullGeometryError):
        parse_wkt("POINT EMPTY")


def test_unsupported_geometry_type():
    unsupported_wkt = "GEOMETRYCOLLECTION(POINT(2 3),LINESTRING(2 3, 3 4))"
    with pytest.raises(InvalidGeometryTypeError):
        parse_wkt(unsupported_wkt)
