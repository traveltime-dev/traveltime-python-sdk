# Travel Time Python SDK

[![PyPI version](https://badge.fury.io/py/traveltimepy.svg)](https://badge.fury.io/py/traveltimepy) [![Unit Tests](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml) [![Python support](https://img.shields.io/badge/python-3.7+-blue.svg)](https://img.shields.io/badge/python-3.7+-blue)

[Travel Time](https://docs.traveltime.com/api/overview/introduction) Python SDK helps users find locations by journey
time rather than using ‘as the crow flies’ distance.  
Time-based searching gives users more opportunities for personalisation and delivers a more relevant search.

## Usage

## Installation

Install Travel Time Python SDK in a `virtualenv` using `pip`. `virtualenv` is a tool to create isolated Python
environments.

`virtualenv` allows to install Travel Time Python SDK without needing system install permissions, and without clashing
with the installed system dependencies.

### Linux/Mac

```
pip3 install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install traveltimepy
```

### Windows

```
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install traveltimepy
```

### Sdk set up

In order to authenticate with Travel Time API, you will have to supply the Application Id and Api Key.

#### Takes:

* app_id: str - Application Id
* api_key: str - Api Key
* limit_per_host: int - Number of simultaneous connections to one host.
* rate_limit: int - Number of searches which can be made in a time window.
* time_window: int - Duration, in seconds, of the time period in which to limit the rate.
* retry_attempts: int - Number of retries for failed requests.
* host: str - TravelTime host, default value is api.traveltimeapp.com.

```python
from traveltimepy import TravelTimeSdk

sdk = TravelTimeSdk(app_id="YOUR_APP_ID", api_key="YOUR_APP_KEY")
```

### [Isochrones (Time Map)](https://docs.traveltime.com/api/reference/isochrones)

Given origin coordinates, find shapes of zones reachable within corresponding travel time.

#### Takes:

* coordinates: List[Coordinates] - Isochrones coordinates.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 3600
* transportation: Union - Transportation mode and related parameters.
* search_range: Range - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.

### JSON response

#### Returns:

* results: List[TimeMapResult] - The list of isochrone shapes.

#### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Driving, Coordinates, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.time_map_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        arrival_time=datetime.now(),
        transportation=Driving()
    )
    print(results)


asyncio.run(main())
```

### GEOJSON response

#### Returns:

* results: FeatureCollection - The list of Features.

#### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Driving, Coordinates, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.time_map_geojson_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        arrival_time=datetime.now(),
        transportation=Driving()
    )
    print(results)


asyncio.run(main())
```

### [Isochrones (Intersection)](https://docs.traveltime.com/api/reference/isochrones)

Given origin coordinates, find intersections of specified shapes.

#### Takes:

* coordinates: List[Coordinates] - Intersection coordinates. The size of list cannot be more than 10.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 3600
* transportation: Union - Transportation mode and related parameters.
* search_range: Range - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.

#### Returns:

* results: List[TimeMapResult] - The list of isochrone shapes.

#### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Driving, Coordinates, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.intersection_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        arrival_time=datetime.now(),
        transportation=Driving()
    )

    print(results)


asyncio.run(main())
```

### [Isochrones (Union)](https://docs.traveltime.com/api/reference/isochrones)

Given origin coordinates, find unions of specified shapes.

Finds the union of specified shapes.

#### Takes:

* coordinates: List[Coordinates] - Union coordinates. The size of list cannot be more than 10.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 3600
* transportation: Union - Transportation mode and related parameters.
* search_range: Range - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.

#### Returns:

* results: List[TimeMapResult] - The list of isochrone shapes.

#### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Driving, Coordinates, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.union_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        arrival_time=datetime.now(),
        transportation=Driving()
    )

    print(results)


asyncio.run(main())
```

### [Distance Matrix (Time Filter)](https://docs.traveltime.com/api/reference/travel-time-distance-matrix)

Given origin and destination points filter out points that cannot be reached within specified time limit. Find out
travel times, distances and costs between an origin and up to 2,000 destination points.

#### Takes:

* locations: List[Locations] - All locations. Location ids must be unique.
* search_ids: Dict[str, List[str]] - Search ids from a target location to destinations. You can define up to 2000
  destinations
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* transportation: Union - Transportation mode and related parameters.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 3600.
* properties: List[Property] - Properties to be returned about the points. Default value is travel_time.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.

#### Returns:

* results: List[TimeFilterResult] - The results list of reachable and unreachable locations.

#### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Location, Coordinates, PublicTransport, Property, FullRange, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    locations = [
        Location(id="London center", coords=Coordinates(lat=51.508930, lng=-0.131387)),
        Location(id="Hyde Park", coords=Coordinates(lat=51.508824, lng=-0.167093)),
        Location(id="ZSL London Zoo", coords=Coordinates(lat=51.536067, lng=-0.153596))
    ]

    results = await sdk.time_filter_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        departure_time=datetime.now(),
        travel_time=3600,
        transportation=PublicTransport(type="bus"),
        properties=[Property.TRAVEL_TIME],
        range=FullRange(enabled=True, max_results=3, width=600)
    )

    print(results)


asyncio.run(main())
```

### [Time Filter (Fast)](https://docs.traveltime.com/api/reference/time-filter-fast)

A very fast version of ```time_filter()```. However, the request parameters are much more limited.

#### Takes:

* locations: List[Locations] - All locations. Location ids must be unique.
* search_ids: Dict[str, List[str]] - Searches from a target location to destinations. You can define up to 100,000
  destinations
* transportation: Union - Transportation mode and related parameters.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 10800. Default value is 3600.
* properties: List[Property] - Properties to be returned about the points. Default value is travel_time.
* one_to_many: boolean - if one_to_many is equal to true, then it'll be a forward search (one to many matrix), false -
  backward search (many to one matrix). Default value is True.

#### Returns:

* results: List[TimeFilterFastResult] - The results list of reachable and unreachable locations.

#### Example:

```python
import asyncio

from traveltimepy import Location, Coordinates, Transportation, TravelTimeSdk

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    
    locations = [
        Location(id="London center", coords=Coordinates(lat=51.508930, lng=-0.131387)),
        Location(id="Hyde Park", coords=Coordinates(lat=51.508824, lng=-0.167093)),
        Location(id="ZSL London Zoo", coords=Coordinates(lat=51.536067, lng=-0.153596))
    ]
    
    results = await sdk.time_filter_fast_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=Transportation(type="public_transport"),
        one_to_many=False
    )
    
    print(results)
    
asyncio.run(main())
```

### [Time Filter Fast (Proto)](https://docs.traveltime.com/api/reference/travel-time-distance-matrix-proto)

A fast version of time filter communicating using [protocol buffers](https://github.com/protocolbuffers/protobuf).

The request parameters are much more limited and only travel time is returned. In addition, the results are only
approximately correct (95% of the results are guaranteed to be within 5% of the routes returned by regular time filter).
This inflexibility comes with a benefit of faster response times (Over 5x faster compared to regular time filter) and
larger limits on the amount of destination points.

#### Takes:

* origin: Coordinates - Origin point.
* destinations: List[Coordinates] - Destination points. Cannot be more than 200,000.
* transportation: ProtoTransportation - Transportation type.
* travel_time: int - Time limit. Maximum value is 7200.
* country: ProtoCountry - Return the results that are within the specified country.
* one_to_many: boolean - if one_to_many is equal to true, then it'll be a forward search (one to many matrix), false -
  backward search (many to one matrix). Default value is True.

#### Returns:

* travel_times: List[int] - The responses are in the form of a list where each position denotes either a travel time (in
  seconds) of a journey, or if negative that the journey from the origin to the destination point is impossible.

#### Example:

```python
import asyncio
from traveltimepy import ProtoCountry, Coordinates, ProtoTransportation, TravelTimeSdk

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    travel_times = await sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793)
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM
    )
    
    print(travel_times)

asyncio.run(main())
```

### [Routes](https://docs.traveltime.com/api/reference/routes)

Returns routing information between source and destinations.

#### Takes:

* locations: List[Locations] - All locations. Location ids must be unique.
* search_ids: Dict[str, List[str]] - Searches from a target location to destinations.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* transportation: Union - Transportation mode and related parameters.
* properties: List[Property] - Properties to be returned about the locations. Default value is travel_time.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.

#### Returns:

* results: List[RoutesResult] - The results list of routes.

#### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Location, Coordinates, PublicTransport, TravelTimeSdk

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    
    locations = [
        Location(id="London center", coords=Coordinates(lat=51.508930, lng=-0.131387)),
        Location(id="Hyde Park", coords=Coordinates(lat=51.508824, lng=-0.167093)),
        Location(id="ZSL London Zoo", coords=Coordinates(lat=51.536067, lng=-0.153596))
    ]

    results = await sdk.routes_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now()
    )
    print(results)

asyncio.run(main())
```

### [Geocoding (Search)](https://docs.traveltime.com/api/reference/geocoding-search)

Match a query string to geographic coordinates.

#### Takes:

* query: str - A query to geocode. Can be an address, a postcode or a venue.
* within_countries: List[str] - Only return the results that are within the specified country.
* limit: int - Expected integer between 1 and 50. Limits amount of results returned to specified number.
* format_name: bool - Format the name field of the geocoding search response to a well formatted, human-readable address
  of the location.
* format_exclude_country: bool - Exclude the country from the formatted name field.
* bounds: Rectangle - Used to limit the results to a bounding box.

#### Returns:

* Matched locations in geojson format

#### Example:

```python
import asyncio
from traveltimepy import TravelTimeSdk

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.geocoding_async(query="Parliament square", limit=30)
    print(results.features)

asyncio.run(main())
```

### [Reverse Geocoding](https://docs.traveltime.com/api/reference/geocoding-reverse)

Match a latitude, longitude pair to an address.

#### Takes:

* lat: float - Latitude
* lng: float - Longitude

#### Returns:

* Matched locations in a geojson format

#### Example:

```python
import asyncio
from traveltimepy import TravelTimeSdk

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.geocoding_reverse_async(lat=51.507281, lng=-0.132120)
    print(results.features)

asyncio.run(main())
```

### [Time Filter (Postcodes)](https://docs.traveltime.com/api/reference/postcode-search)

Find reachable postcodes from origin (or to destination) and get statistics about such postcodes. Currently only
supports United Kingdom.

#### Takes:

* coordinates: List[Coordinates] - Location coordinates.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 1800
* transportation: Union - Transportation mode and related parameters.
* properties: List[Property] - Properties to be returned about the postcodes. Default value is travel_time.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.

#### Returns:

* results: List[PostcodesResult] - The results list of postcodes.

#### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Coordinates, PublicTransport, TravelTimeSdk

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.postcodes_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport()
    )
    
    print(results)

asyncio.run(main())
```

### [Time Filter (Postcode Districts)](https://docs.traveltime.com/api/reference/postcode-district-filter)

Find districts that have a certain coverage from origin (or to destination) and get statistics about postcodes within
such districts. Currently only supports United Kingdom.

#### Takes:

* coordinates: List[Coordinates] - Location coordinates.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 1800
* transportation: Union - Transportation mode and related parameters.
* reachable_postcodes_threshold: float - A number between 0.0 and 1.0. Default value is 0.1. For example, if 0.5 is
  used, only districts that have at least 50% postcodes that can be reached within the given travel_time will be
  included in the response. 0 will return districts that have at least a single reachable postcode.
* properties: List[Property] - Properties to be returned about the districts. Default value is travel_time_all.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.

#### Returns:

* results: List[DistrictsResult] - The results list of districts.

#### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Coordinates, PublicTransport, TravelTimeSdk

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.postcodes_districts_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport()
    )
    
    print(results)
    
asyncio.run(main())

```

### [Time Filter (Postcode Sectors)](https://docs.traveltime.com/api/reference/postcode-sector-filter)

Find sectors that have a certain coverage from origin (or to destination) and get statistics about postcodes within such
sectors. Currently only supports United Kingdom.

#### Takes:

* coordinates: List[Coordinates] - Location coordinates.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 1800
* transportation: Union - Transportation mode and related parameters.
* reachable_postcodes_threshold: float - A number between 0.0 and 1.0. Default value is 0.1. For example, if 0.5 is
  used, only sectors that have at least 50% postcodes that can be reached within the given travel_time will be included
  in the response. 0 will return sectors that have at least a single reachable postcode.
* properties: List[Property] - Properties to be returned about the sectors. Default value is travel_time_all.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.

#### Returns:

* results: List[SectorsResult] - The results list of postcode sectors.

#### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Coordinates, PublicTransport, TravelTimeSdk, ZonesProperty

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.postcodes_sectors_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
        properties=[ZonesProperty.TRAVEL_TIME_REACHABLE, ZonesProperty.TRAVEL_TIME_ALL]
    )
    
    print(results)
asyncio.run(main())
```

### [Map Info](https://docs.traveltime.com/api/reference/map-info)

Returns information about currently supported countries.

It is useful when you have an application that can do searches in any country that we support, you can use Supported
Locations to get the map name for a certain point and then use this endpoint to check what features are available for
that map. That way you could show fares for routes in the maps that support it.

#### Returns:

* maps: List[Map]
* name - An internal map id. The first two characters usually correspond to the ISO 3166-2 standard (e.g th, ie)
  sometimes followed by additional characters (e.g ca_pst, us_pst). To get features of a specific map, use the map
  info endpoint.
* features - Features that are supported in the specified map

#### Example:

```python
import asyncio
from traveltimepy import TravelTimeSdk

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.map_info_async()
    print(results)

asyncio.run(main())
```

### [Supported Locations](https://docs.traveltime.com/api/reference/supported-locations)

Find out what points are supported by our api. The returned map name for a point can be used to determine what features
are supported.

#### Takes:

* locations: List[Location] - Each location requires an id and lat/lng values

#### Returns:

* locations: List[SupportedLocation]
* id - Location id that you specified in the request.
* map_name - An internal map id. The first two characters usually correspond to the ISO 3166-2 standard (e.g th, ie)
  sometimes followed by additional characters (e.g ca_pst, us_pst). To get features of a specific map, use the map
  info endpoint.
* additional_map_names - In case the location is in more than one map, other map ids are listed here.
* unsupported_locations: List[str] - List that contains ids of locations that are unsupported.

#### Example:

```python
import asyncio
from traveltimepy import Location, Coordinates, TravelTimeSdk

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    
    locations = [
        Location(id="Kaunas", coords=Coordinates(lat=54.900008, lng=23.957734)),
        Location(id="London", coords=Coordinates(lat=51.506756, lng=-0.12805)),
        Location(id="Bangkok", coords=Coordinates(lat=13.761866, lng=100.544818)),
        Location(id="Lisbon", coords=Coordinates(lat=38.721869, lng=-9.138549)),
    ]
    
    results = await sdk.supported_locations_async(locations)
    
    print(results.locations)
    print(results.unsupported_locations)

asyncio.run(main())
```
