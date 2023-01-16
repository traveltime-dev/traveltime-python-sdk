
def test_map_info(sdk):
    maps = sdk.map_info()
    assert len(maps) > 0
