from typing import Optional


class MockResponse:
    def __init__(self, data: Optional[str], status_code: int) -> None:
        self.data = data
        self.status_code = status_code

    @property
    def text(self) -> Optional[str]:
        return self.data

# {"departure_searches":[{"id":"search_1","coords":{"lat":51.507609,"lng":-0.128315},"departure_time":"2022-11-24T12:00:00","travel_time":900,"transportation":{"type":"public_transport","pt_change_delay":null,"walking_time":null,"max_changes":null},"range":null},{"id":"search_2","coords":{"lat":51.507609,"lng":-0.128315},"departure_time":"2022-11-24T12:00:00","travel_time":900,"transportation":{"type":"driving","disable_border_crossing":null},"range":null}],"arrival_searches":[{"id":"search_3","coords":{"lat":51.507609,"lng":-0.128315},"arrival_time":"2022-11-24T12:00:00","travel_time":900,"transportation":{"type":"public_transport","pt_change_delay":null,"walking_time":null,"max_changes":null},"range":{"enabled":true,"width":3600}}],"unions":[{"id":"search_4","search_ids":["search_2","search_3"]}],"intersections":[{"id":"search_5","search_ids":["search_2","search_3"]}]}
# {"departure_searches":[{"id":"search_1","coords":{"lat":51.507609,"lng":-0.128315},"departure_time":"2022-11-24T12:00:00","travel_time":900,"transportation":{"type":"public_transport"},"range":null},{"id":"search_2","coords":{"lat":51.507609,"lng":-0.128315},"departure_time":"2022-11-24T12:00:00","travel_time":900,"transportation":{"type":"driving"},"range":null}],"arrival_searches":[{"id":"search_3","coords":{"lat":51.507609,"lng":-0.128315},"arrival_time":"2022-11-24T12:00:00","travel_time":900,"transportation":{"type":"public_transport"},"range":{"enabled":true,"width":3600}}],"unions":[{"id":"search_4","search_ids":["search_2","search_3"]}],"intersections":[{"id":"search_5","search_ids":["search_2","search_3"]}]}
class UrlInfo:
    def __init__(self, request_file: Optional[str], response_file: str, status_code: int) -> None:
        self.request_file = request_file
        self.response_file = response_file
        self.status_code = status_code

    def check_request_data(self, request_data: str) -> bool:
        if self.request_file is not None:
            expected_request = read_file(f'resources/requests/{self.request_file}').replace(" ", "")
            cur_request = request_data.replace(" ", "")
            return expected_request == cur_request
        else:
            return True

    def response_file_path(self) -> str:
        return f'resources/responses/{self.response_file}'


urls = {
    'https://api.traveltimeapp.com/v4/map-info': UrlInfo(None, 'map_info.json', 200),
    'https://api.traveltimeapp.com/v4/time-map': UrlInfo('time_map.json', 'time_map.json', 200),
    'https://api.traveltimeapp.com/v4/time-filter': UrlInfo('time_filter.json', 'time_filter.json', 200)
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
