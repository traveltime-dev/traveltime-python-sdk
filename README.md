# Travel Time Python SDK
[![PyPI version](https://badge.fury.io/py/traveltimepy.svg)](https://badge.fury.io/py/traveltimepy) [![Unit Tests](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml) [![Python support](https://img.shields.io/badge/python-3.7+-blue.svg)](https://img.shields.io/badge/python-3.7+-blue)

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
from datetime import datetime

from traveltimepy.dto import Coordinates
from traveltimepy.dto.requests import Range
from traveltimepy.dto.requests.time_map import DepartureSearch, ArrivalSearch, Union, Intersection
from traveltimepy.transportation import PublicTransport, Driving

departure_search1 = DepartureSearch(
    id='search_1',
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    departure_time=datetime.now(),
    travel_time=900,
    transportation=PublicTransport()
)
departure_search2 = DepartureSearch(
    id='search_2',
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    departure_time=datetime.now(),
    travel_time=900,
    transportation=Driving()
)
arrival_search = ArrivalSearch(
    id='search_3',
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    arrival_time=datetime.now(),
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
from datetime import datetime

from traveltimepy.dto import Location, Coordinates
from traveltimepy.dto.requests import FullRange, Property
from traveltimepy.dto.requests.time_filter import DepartureSearch, ArrivalSearch
from traveltimepy.transportation import PublicTransport

locations = [
    Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
    Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
    Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
]

departure_search = DepartureSearch(
    id='forward search example',
    arrival_location_ids=['Hyde Park', 'ZSL London Zoo'],
    departure_location_id='London center',
    departure_time=datetime.now(),
    travel_time=3600,
    transportation=PublicTransport(type='bus'),
    properties=[Property.TRAVEL_TIME],
    full_range=FullRange(enabled=True, max_results=3, width=600)
)

arrival_search = ArrivalSearch(
    id='backward search example',
    departure_location_ids=['Hyde Park', 'ZSL London Zoo'],
    arrival_location_id='London center',
    arrival_time=datetime.now(),
    travel_time=3800,
    transportation=PublicTransport(type='bus'),
    properties=[Property.TRAVEL_TIME, Property.FARES, Property.ROUTE],
)

response = sdk.time_filter(locations, [departure_search], [arrival_search])
```


### [Time Filter (Fast)](https://traveltime.com/api/reference/time-filter-fast)

A very fast version of time_filter()

```python
from traveltimepy.dto import Location, Coordinates
from traveltimepy.dto.requests import Property
from traveltimepy.dto.requests.time_filter_fast import Transportation, ManyToOne, OneToMany

locations = [
    Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
    Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
    Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
]
many_to_one = ManyToOne(
    id='many-to-one search example',
    departure_location_ids=['Hyde Park', 'ZSL London Zoo'],
    arrival_location_id='London center',
    transportation=Transportation(type='public_transport'),
    arrival_time_period='weekday_morning',
    travel_time=1900,
    properties=[Property.TRAVEL_TIME, Property.FARES]
)
one_to_many = OneToMany(
    id='one-to-many search example',
    arrival_location_ids=['Hyde Park', 'ZSL London Zoo'],
    departure_location_id='London center',
    transportation=Transportation(type='public_transport'),
    arrival_time_period='weekday_morning',
    travel_time=1900,
    properties=[Property.TRAVEL_TIME, Property.FARES]
)

response = sdk.time_filter_fast(locations, [many_to_one], [one_to_many])
```

### Time Filter Fast (Proto)

A fast version of time filter communicating using [protocol buffers](https://github.com/protocolbuffers/protobuf).

The request parameters are much more limited and only travel time is returned. In addition, the results are only approximately correct (95% of the results are guaranteed to be within 5% of the routes returned by regular time filter).

This inflexibility comes with a benefit of faster response times (Over 5x faster compared to regular time filter) and larger limits on the amount of destination points.

Body attributes:
* origin_coordinates: Origin point.
* destination_coordinates: Destination points. Cannot be more than 200,000.
* transportation: Transportation type.
* travel_time: Time limit;
* country: Return the results that are within the specified country

```python
from traveltimepy.dto import Coordinates

from traveltimepy.dto.requests.time_filter_proto import OneToMany, Transportation, Country

one_to_many = OneToMany(
    origin_coordinates=Coordinates(lat=51.425709, lng=-0.122061),
    destination_coordinates=[
        Coordinates(lat=51.348605, lng=-0.314783),
        Coordinates(lat=51.337205, lng=-0.315793)
    ],
    transportation=Transportation.DRIVING,
    travel_time=7200,
    country=Country.UNITED_KINGDOM
)

response = sdk.time_filter_proto(one_to_many)
```

The responses are in the form of a list where each position denotes either a
travel time (in seconds) of a journey, or if negative that the journey from the
origin to the destination point is impossible.


### [Routes](https://traveltime.com/docs/api/reference/routes)

Returns routing information between source and destinations.

```python
from datetime import datetime

from traveltimepy.dto import Location, Coordinates
from traveltimepy.dto.requests import FullRange, Property
from traveltimepy.dto.requests.routes import DepartureSearch, ArrivalSearch
from traveltimepy.transportation import PublicTransport

locations = [
    Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
    Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
    Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
]

departure_search = DepartureSearch(
    id='departure search example',
    arrival_location_ids=['Hyde Park', 'ZSL London Zoo'],
    departure_location_id='London center',
    departure_time=datetime.now(),
    transportation=PublicTransport(type='bus'),
    properties=[Property.TRAVEL_TIME],
    full_range=FullRange(enabled=True, max_results=3, width=600)
)

arrival_search = ArrivalSearch(
    id='arrival search example',
    departure_location_ids=['Hyde Park', 'ZSL London Zoo'],
    arrival_location_id='London center',
    arrival_time=datetime.now(),
    transportation=PublicTransport(type='bus'),
    properties=[Property.TRAVEL_TIME, Property.FARES, Property.ROUTE],
)

response = sdk.routes(locations, [departure_search], [arrival_search])
```

### [Time Filter (Postcodes)](https://traveltime.com/docs/api/reference/postcode-search)
Find reachable postcodes from origin (or to destination) and get statistics about such postcodes.

```python
from datetime import datetime

from traveltimepy.dto import Coordinates
from traveltimepy.dto.requests import Property
from traveltimepy.dto.requests.postcodes import DepartureSearch, ArrivalSearch
from traveltimepy.transportation import PublicTransport

departure_search = DepartureSearch(
    id='public transport from Trafalgar Square',
    departure_time=datetime.now(),
    travel_time=1800,
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    transportation=PublicTransport(),
    properties=[Property.TRAVEL_TIME, Property.DISTANCE]
)

arrival_search = ArrivalSearch(
    id='public transport to Trafalgar Square',
    arrival_time=datetime.now(),
    travel_time=1800,
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    transportation=PublicTransport(),
    properties=[Property.TRAVEL_TIME, Property.DISTANCE]
)

response = sdk.postcodes([departure_search], [arrival_search])
```

### [Time Filter (Postcode Sectors)](https://traveltime.com/docs/api/reference/postcode-sector-filter)
Find sectors that have a certain coverage from origin (or to destination) and get statistics about postcodes within such sectors.

```python
from datetime import datetime
from traveltimepy.dto import Coordinates
from traveltimepy.dto.requests.zones import DepartureSearch, ArrivalSearch, Property
from traveltimepy.transportation import PublicTransport

departure_search = DepartureSearch(
    id='public transport from Trafalgar Square',
    departure_time=datetime.now(),
    travel_time=200,
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    reachable_postcodes_threshold=0.1,
    transportation=PublicTransport(),
    properties=[Property.TRAVEL_TIME_ALL, Property.TRAVEL_TIME_REACHABLE]
)

arrival_search = ArrivalSearch(
    id='public transport to Trafalgar Square',
    arrival_time=datetime.now(),
    travel_time=200,
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    reachable_postcodes_threshold=0.1,
    transportation=PublicTransport(),
    properties=[Property.COVERAGE]
)

response = sdk.sectors([departure_search], [arrival_search])
```

### [Time Filter (Postcode Districts)](https://traveltime.com/docs/api/reference/postcode-district-filter)
Find reachable postcodes from origin (or to destination) and get statistics about such postcodes.

```python
from datetime import datetime
from traveltimepy.dto import Coordinates
from traveltimepy.dto.requests.zones import DepartureSearch, ArrivalSearch, Property
from traveltimepy.transportation import PublicTransport

departure_search = DepartureSearch(
    id='public transport from Trafalgar Square',
    departure_time=datetime.now(),
    travel_time=200,
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    reachable_postcodes_threshold=0.1,
    transportation=PublicTransport(),
    properties=[Property.TRAVEL_TIME_ALL, Property.TRAVEL_TIME_REACHABLE]
)

arrival_search = ArrivalSearch(
    id='public transport to Trafalgar Square',
    arrival_time=datetime.now(),
    travel_time=200,
    coords=Coordinates(lat=51.507609, lng=-0.128315),
    reachable_postcodes_threshold=0.1,
    transportation=PublicTransport(),
    properties=[Property.COVERAGE]
)

response = sdk.districts([departure_search], [arrival_search])
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
from traveltimepy.dto import Location, Coordinates

locations = [
    Location(id='Kaunas', coords=Coordinates(lat=54.900008, lng=23.957734)),
    Location(id='London', coords=Coordinates(lat=51.506756, lng=-0.12805)),
    Location(id='Bangkok', coords=Coordinates(lat=13.761866, lng=100.544818)),
    Location(id='Lisbon', coords=Coordinates(lat=38.721869, lng=-9.138549)),
]
response = sdk.supported_locations(locations)
```
