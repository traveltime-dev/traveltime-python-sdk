import dataclasses
import json
from datetime import datetime

import requests

from traveltime.errors import ApiError


def send_request(path, headers, body=None, query=None):
    url = "/".join(["https://api.traveltimeapp.com", 'v4', path])
    if body is None:
        resp = requests.get(url=url, headers=headers, params=query)
    else:
        resp = requests.post(url=url, headers=headers, data=to_json(body))

    try:
        parsed = resp.json()
    except:
        raise ApiError('Travel Time API did not return json') from None

    if resp.status_code != 200:
        msg = "Travel Time API request failed [{}]\n{}\nError code: {}\n<{}>\n".format(
            resp.status_code,
            parsed['description'],
            parsed['error_code'],
            parsed['documentation_link']
        )
        if 'additional_info' in parsed:
            for k, v in parsed['additional_info'].items():
                msg += k + ": " + str(v) + "\n"

        raise ApiError(msg)

    return parsed


def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()


def to_json(value):
    return json.dumps(dataclasses.asdict(value), default=default)
