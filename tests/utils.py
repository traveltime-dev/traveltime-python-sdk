from typing import Optional


class MockResponse:
    def __init__(self, json_data: Optional[str], status_code: int) -> None:
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> str:
        return self.json_data


def mocked_requests(*args, **kwargs):
    url = kwargs.get('url')
    if url == 'https://api.traveltimeapp.com/v4/map-info':
        json_data = read_file("resources/responses/map_info.json")
        return MockResponse(json_data, 200)
    elif url == 'https://api.traveltimeapp.com/v4/time_map':
        json_data = read_file("resources/responses/time_map.json")
        return MockResponse(json_data, 200)
    else:
        return MockResponse(None, 404)


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read().replace('\n', '')
