# Travel Time Python SDK
[![PyPI version](https://badge.fury.io/py/traveltimepy.svg)](https://badge.fury.io/py/traveltimepy) [![Unit Tests](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml)

Travel Time Python SDK helps users find locations by journey time rather than using ‘as the crow flies’ distance.  
Time-based searching gives users more opportunities for personalisation and delivers a more relevant search.

## Usage

### Authentication

In order to authenticate with Travel Time API, you will have to supply the Application Id and Api Key.

```python
from traveltimepy.sdk import TravelTimeSdk

sdk = TravelTimeSdk('YOUR_API_ID', 'YOUR_API_KEY')
```

### [Isochrones (Time Map)](https://traveltime.com/docs/api/reference/isochrones)

Given origin coordinates, find shapes of zones reachable within corresponding travel time.

```python
departure_search1 = DepartureSearch(
    id='search_1',
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    departure_time=datetime(2022, 11, 24, 12, 0, 0),
    travel_time=900,
    transportation=PublicTransport()
)
departure_search2 = DepartureSearch(
    id='search_2',
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    departure_time=datetime(2022, 11, 24, 12, 0, 0),
    travel_time=900,
    transportation=Driving()
)
arrival_search = ArrivalSearch(
    id='search_3',
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    arrival_time=datetime(2022, 11, 24, 12, 0, 0),
    travel_time=900,
    transportation=PublicTransport(),
    range=Range(enabled=True, width=3600)
)
union = Union(
    id='search_4',
    search_ids=['search_2', 'search_3']
)
intersection = Intersection(
    id='search_5',
    search_ids=['search_2', 'search_3']
)
response = sdk.time_map(
    [arrival_search],
    [departure_search1, departure_search2],
    [union],
    [intersection]
)
```

### [Distance Matrix (Time Filter)](https://traveltime.com/docs/api/reference/distance-matrix)

Given origin and destination points filter out points that cannot be reached within specified time limit.

```python
locations = [
    Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
    Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
    Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
]

departure_search = DepartureSearch(
    id='forward search example',
    arrival_location_ids=['Hyde Park', 'ZSL London Zoo'],
    departure_location_id='London center',
    departure_time=datetime(2022, 11, 24, 12, 0, 0),
    travel_time=3600,
    transportation=PublicTransport(type='bus'),
    properties=[Property.TRAVEL_TIME],
    full_range=FullRange(enabled=True, max_results=3, width=600)
)

arrival_search = ArrivalSearch(
    id='backward search example',
    departure_location_ids=['Hyde Park', 'ZSL London Zoo'],
    arrival_location_id='London center',
    arrival_time=datetime(2022, 11, 24, 12, 0, 0),
    travel_time=3800,
    transportation=PublicTransport(type='bus'),
    properties=[Property.TRAVEL_TIME, Property.FARES, Property.ROUTE],
)

response = sdk.time_filter(locations, [departure_search], [arrival_search])
```

### [Routes](https://traveltime.com/docs/api/reference/routes)

Returns routing information between source and destinations.

```python
locations = [
    Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
    Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
    Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
]

departure_search = DepartureSearch(
    id='departure search example',
    arrival_location_ids=['Hyde Park', 'ZSL London Zoo'],
    departure_location_id='London center',
    departure_time=datetime(2022, 11, 24, 12, 0, 0),
    transportation=PublicTransport(type='bus'),
    properties=[Property.TRAVEL_TIME],
    full_range=FullRange(enabled=True, max_results=3, width=600)
)

arrival_search = ArrivalSearch(
    id='arrival search example',
    departure_location_ids=['Hyde Park', 'ZSL London Zoo'],
    arrival_location_id='London center',
    arrival_time=datetime(2022, 11, 24, 12, 0, 0),
    transportation=PublicTransport(type='bus'),
    properties=[Property.TRAVEL_TIME, Property.FARES, Property.ROUTE],
)

response = sdk.routes(locations, [departure_search], [arrival_search])
```

### [Geocoding (Search)](https://traveltime.com/docs/api/reference/geocoding-search)

Match a query string to geographic coordinates.

```python
response = sdk.geocoding(query='Parliament square', limit=30)
```

### [Reverse Geocoding](https://traveltime.com/docs/api/reference/geocoding-reverse)

Match a latitude, longitude pair to an address.

```python
response = sdk.geocoding_reverse(lat=51.507281, lng=-0.132120)
```

### [Map Info](https://traveltime.com/docs/api/reference/map-info)

Get information about currently supported countries.

```python
response = sdk.map_info()
```

### [Supported Locations](https://traveltime.com/docs/api/reference/supported-locations)

Find out what points are supported by the api.

```python
locations = [
    Location(id='Kaunas', coords=Coordinates(lat=54.900008, lng=23.957734)),
    Location(id='London', coords=Coordinates(lat=51.506756, lng=-0.12805)),
    Location(id='Bangkok', coords=Coordinates(lat=13.761866, lng=100.544818)),
    Location(id='Lisbon', coords=Coordinates(lat=38.721869, lng=-9.138549)),
]
response = sdk.supported_locations(locations)
```
