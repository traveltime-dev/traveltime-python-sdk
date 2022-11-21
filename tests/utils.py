import json

from requests import Response


def mocked_requests(*args, **kwargs):
    response_content = None
    request_url = kwargs.get('url', None)
    if request_url == 'aurl':
        response_content = json.dumps('a response')
    elif request_url == 'burl':
        response_content = json.dumps('b response')
    elif request_url == 'curl':
        response_content = json.dumps('c response')
    #https://api.traveltimeapp.com/v4/time-map
    response = Response()
    response.status_code = 200
    response._content = read_file("tests/resources/time_map.json")
    print(response.json())
    return response


def read_file(path):
    with open(path, 'r') as file:
        return file.read().replace('\n', '')
