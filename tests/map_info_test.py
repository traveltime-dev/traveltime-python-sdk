
def test_map_info(sdk):
    response = sdk.map_info()
    assert len(response.maps) > 0
