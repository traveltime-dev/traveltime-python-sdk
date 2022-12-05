from typing import Optional


class MockResponse:
    def __init__(self, data: Optional[str], status_code: int) -> None:
        self.data = data
        self.status_code = status_code

    @property
    def text(self) -> Optional[str]:
        return self.data


class UrlInfo:
    def __init__(self, request_file: Optional[str], response_file: str, status_code: int) -> None:
        self.request_file = request_file
        self.response_file = response_file
        self.status_code = status_code

    def check_request_data(self, request_data: str) -> bool:
        if self.request_file is not None:
            expected_request = read_file(f'tests/resources/requests/{self.request_file}').replace(' ', '')
            cur_request = request_data.replace(' ', '')
            return expected_request == cur_request
        else:
            return True

    def response_file_path(self) -> str:
        return f'tests/resources/responses/{self.response_file}'


urls = {
    'https://api.traveltimeapp.com/v4/map-info': UrlInfo(None, 'map_info.json', 200),
    'https://api.traveltimeapp.com/v4/time-map': UrlInfo('time_map.json', 'time_map.json', 200),
    'https://api.traveltimeapp.com/v4/routes': UrlInfo('routes.json', 'routes.json', 200),
    'https://api.traveltimeapp.com/v4/time-filter': UrlInfo('time_filter.json', 'time_filter.json', 200),
    'https://api.traveltimeapp.com/v4/geocoding/search': UrlInfo(None, 'geocoding.json', 200),
    'https://api.traveltimeapp.com/v4/geocoding/reverse': UrlInfo(None, 'geocoding.json', 200),
    'https://api.traveltimeapp.com/v4/time-filter/postcodes': UrlInfo('postcodes.json', 'postcodes.json', 200),
    'https://api.traveltimeapp.com/v4/time-filter/postcode-districts': UrlInfo('districts.json', 'districts.json', 200),
    'https://api.traveltimeapp.com/v4/time-filter/postcode-sectors': UrlInfo('sectors.json', 'sectors.json', 200),
    'https://api.traveltimeapp.com/v4/time-filter/fast': UrlInfo('time_filter_fast.json', 'time_filter_fast.json', 200),
    'https://api.traveltimeapp.com/v4/supported-locations': UrlInfo(
        'supported_locations.json',
        'supported_locations.json',
        200
    )
}


def mocked_requests(*args, **kwargs):
    url = kwargs.get('url')
    request_data = kwargs.get('data')
    url_info = urls.get(url)

    if url_info.check_request_data(request_data):
        response = read_file(url_info.response_file_path())
        return MockResponse(response, 200)
    else:
        return MockResponse(None, 404)


def check_request_data(path: str, data: str) -> bool:
    request = read_file(path)
    return data == request


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read().replace('\n', '')
