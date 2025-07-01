import pytest  # noqa

from traveltimepy.requests.common import Coordinates
from traveltimepy.wkt import (
    PointModel,
    LineStringModel,
    PolygonModel,
    MultiPointModel,
    MultiLineStringModel,
    MultiPolygonModel,
)

# Updated mock data for LineStringModel with two distinct points
mock_point1 = PointModel(coordinates=Coordinates(lat=10, lng=20))
mock_point2 = PointModel(coordinates=Coordinates(lat=30, lng=40))
mock_linestring = LineStringModel(coordinates=[mock_point1, mock_point2])
mock_polygon = PolygonModel(exterior=mock_linestring, interiors=[mock_linestring])
mock_multipoint = MultiPointModel(coordinates=[mock_point1, mock_point2])
mock_multilinestring = MultiLineStringModel(
    coordinates=[mock_linestring, mock_linestring]
)
mock_multipolygon = MultiPolygonModel(coordinates=[mock_polygon])


# Test functions
def test_pointmodel_pretty_print(capsys):
    mock_point1.pretty_print()
    captured = capsys.readouterr()
    assert captured.out == "POINT: 10.0, 20.0\n"


def test_linestringmodel_pretty_print(capsys):
    mock_linestring.pretty_print()
    captured = capsys.readouterr()
    assert captured.out == "LINE STRING:\n\tPOINT: 10.0, 20.0\n\tPOINT: 30.0, 40.0\n"


def test_polygonmodel_pretty_print(capsys):
    mock_polygon.pretty_print()
    captured = capsys.readouterr()
    assert captured.out == (
        "POLYGON:\n\tEXTERIOR:\n\t\tLINE STRING:\n\t\t\tPOINT: 10.0, 20.0\n\t\t\tPOINT: 30.0, 40.0\n"
        "\tINTERIORS:\n\t\tLINE STRING:\n\t\t\tPOINT: 10.0, 20.0\n\t\t\tPOINT: 30.0, 40.0\n"
    )


def test_multipointmodel_pretty_print(capsys):
    mock_multipoint.pretty_print()
    captured = capsys.readouterr()
    assert captured.out == "MULTIPOINT:\n\tPOINT: 10.0, 20.0\n\tPOINT: 30.0, 40.0\n"


def test_multilinestringmodel_pretty_print(capsys):
    mock_multilinestring.pretty_print()
    captured = capsys.readouterr()
    assert captured.out == (
        "MULTILINESTRING:\n\tLINE STRING:\n\t\tPOINT: 10.0, 20.0\n\t\tPOINT: 30.0, 40.0\n"
        "\tLINE STRING:\n\t\tPOINT: 10.0, 20.0\n\t\tPOINT: 30.0, 40.0\n"
    )


def test_multipolygonmodel_pretty_print(capsys):
    mock_multipolygon.pretty_print()
    captured = capsys.readouterr()
    assert captured.out == (
        "MULTIPOLYGON:\n\tPOLYGON:\n\t\tEXTERIOR:\n\t\t\tLINE STRING:\n\t\t\t\tPOINT: 10.0, 20.0\n\t\t\t\tPOINT: 30.0, 40.0\n"
        "\t\tINTERIORS:\n\t\t\tLINE STRING:\n\t\t\t\tPOINT: 10.0, 20.0\n\t\t\t\tPOINT: 30.0, 40.0\n"
    )
