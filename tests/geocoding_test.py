
def test_geocoding_search(sdk):
    response = sdk.geocoding(query='Parliament square', limit=30, within_countries=['gb', 'de'])
    assert len(response.features) > 0
    assert len(response.features) < 31


def test_geocoding_reverse(sdk):
    response = sdk.geocoding_reverse(lat=51.507281, lng=-0.132120, within_countries=['gb', 'de'])
    assert len(response.features) > 0
