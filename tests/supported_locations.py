from traveltimepy import Location, Coordinates


def test_supported_locations(sdk):
    locations = [
        Location(id='Kaunas', coords=Coordinates(lat=54.900008, lng=23.957734)),
        Location(id='London', coords=Coordinates(lat=51.506756, lng=-0.12805)),
        Location(id='Bangkok', coords=Coordinates(lat=13.761866, lng=100.544818)),
        Location(id='Lisbon', coords=Coordinates(lat=38.721869, lng=-9.138549)),
        Location(id='Unsupported', coords=Coordinates(lat=68.721869, lng=-9.138549))
    ]
    response = sdk.supported_locations(locations)
    assert len(response.locations) == 4
    assert len(response.unsupported_locations) == 1
