import os
import requests

class APIError(Exception):
    pass

def build_body(args):

  body = {key: value for (key, value) in args.items() if not value is None}

  for k,v in body.items():
    if isinstance(v, dict):
      body[k] = [v]
  
  return body

def get_api_headers():

  ttid = os.environ.get('TRAVELTIME_ID', None)
  ttkey = os.environ.get('TRAVELTIME_KEY', None)

  if ttid is None:
    raise APIError("Please set env var TRAVELTIME_ID to your Travel Time Application Id")
  if ttkey is None:
    raise APIError("Please set env var TRAVELTIME_KEY to your Travel Time Api Key")

  return {'X-Application-Id': ttid, 'X-Api-Key': ttkey, 'User-Agent': 'Travel Time Python SDK'}


def traveltime_api(path, body = None, query = None):

  url = "/".join(["https://api.traveltimeapp.com", 'v4'] + path)
  
  if body is None:
    resp = requests.get(url = url, headers = get_api_headers(), params = query)
  else:
    resp = requests.post(url = url, headers = get_api_headers(), json = body)
      
  try:
    parsed = resp.json()
  except:
    raise APIError('Travel Time API did not return json') from None
  
  if resp.status_code != 200:
    msg = "Travel Time API request failed [{}]\n{}\nError code: {}\n<{}>\n".format(
      resp.status_code,
      parsed['description'],
      parsed['error_code'],
      parsed['documentation_link']
    )
    if 'additional_info' in parsed:
      for k,v in parsed['additional_info'].items():
        msg += k + ": " + str(v) + "\n"

    raise APIError(msg)

  return parsed


