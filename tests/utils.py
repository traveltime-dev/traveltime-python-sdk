from typing import Optional


class MockResponse:
    def __init__(self, data: Optional[str], status_code: int) -> None:
        self.data = data
        self.status_code = status_code

    @property
    def text(self) -> Optional[str]:
        return self.data


def mocked_requests(*args, **kwargs):
    url = kwargs.get('url')
    if url == 'https://api.traveltimeapp.com/v4/time-map':
        json_data = read_file("resources/responses/time_map.json")
        return MockResponse(json_data, 200)
    else:
        return MockResponse(None, 404)


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read().replace('\n', '')
