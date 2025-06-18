import pytest  # noqa

from traveltimepy.requests.common import Coordinates
from traveltimepy.wkt import LineStringModel, PointModel

mock_point1 = PointModel(coordinates=Coordinates(lat=10, lng=20))
mock_point2 = PointModel(coordinates=Coordinates(lat=30, lng=40))


def test_linestring_minimum_coordinates_valid():
    # Create LineStringModel with two valid coordinates
    linestring = LineStringModel(coordinates=[mock_point1, mock_point2])
    assert len(linestring.coordinates) == 2


def test_linestring_minimum_coordinates_invalid():
    # Test LineStringModel with less than two coordinates
    with pytest.raises(ValueError) as excinfo:
        LineStringModel(coordinates=[mock_point1])
    assert "LineString must have at least 2 coordinates." in str(excinfo.value)
