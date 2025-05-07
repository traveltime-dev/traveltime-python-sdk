# Travel Time Python SDK

[![PyPI version](https://badge.fury.io/py/traveltimepy.svg)](https://badge.fury.io/py/traveltimepy) [![Unit Tests](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml) [![Python support](https://img.shields.io/badge/python-3.8+-blue.svg)](https://img.shields.io/badge/python-3.8+-blue)

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
* timeout: int - Maximum session time until timeout. Default value is 300 (5 minutes).

```python
from traveltimepy import TravelTimeSdk

sdk = TravelTimeSdk(app_id="YOUR_APP_ID", api_key="YOUR_APP_KEY")
```

### [Isochrones (Time Map)](https://docs.traveltime.com/api/reference/isochrones)

Given origin coordinates, find shapes of zones reachable within corresponding travel time.

##### Takes:

* coordinates: List[Coordinates] - Isochrones coordinates.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 3600
* [transportation](#transportation): Union - Transportation mode and related parameters.
* search_range: Range - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.
* [level_of_detail](#level-of-detail): LevelOfDetail - When enabled, allows the user to specify how detailed the isochrones should be.
* remove_water_bodies: bool - if set to true (default) - returned shape will not cover large nearby water bodies.
False - returned shape may cover nearby water bodies like large lakes, wide rivers and seas.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* [polygons_filter](#polygons-filter): PolygonsFilter - Specifies polygon filter of a single shape.
* [render_mode](#render-mode): RenderMode - Specifies which render mode should be used.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

#### JSON response

##### Returns:

* results: List[TimeMapResult] - The list of isochrone shapes.

##### Example:

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

#### GEOJSON response

##### Returns:

* results: FeatureCollection - The list of Features.

##### Example:

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

#### WKT response

##### Returns:

* results: TimeMapWKTResponse - TimeMapWktResponse with isochrone shapes.

##### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Driving, Coordinates, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    response = await sdk.time_map_wkt_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        arrival_time=datetime.now(),
        transportation=Driving()
    )
    response.pretty_print() # for a custom formatted response 
    
    print(response) # default Python print

    
asyncio.run(main())
```

#### WKT_NO_HOLES response

##### Returns:

* results: TimeMapWKTResponse - TimeMapWktResponse with isochrone shapes (no holes).

##### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Driving, Coordinates, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    response = await sdk.time_map_wkt_no_holes_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        arrival_time=datetime.now(),
        transportation=Driving()
    )
    response.pretty_print() # for a custom formatted response 

    print(response) # default Python print


asyncio.run(main())
```

### [Time Map (Fast)](https://docs.traveltime.com/api/reference/isochrones-fast)

A very fast version of `time_map()`. However, the request parameters are much more limited.

##### Takes:

* coordinates: List[Coordinates] - Isochrones coordinates.
* [transportation]: Transportation - Transportation mode and related parameters.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 10800. Default value is 3600.
* one_to_many: boolean - returns the reachable area for journeys arriving at the chosen arrival location if false,
returns the reachable area for journeys departing from the chosen departure location if true.
* [level_of_detail](#level-of-detail): LevelOfDetail - When enabled, allows the user to specify how detailed the isochrones should be.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* [polygons_filter](#polygons-filter): PolygonsFilter - Specifies polygon filter of a single shape.
* [render_mode](#render-mode): RenderMode - Specifies which render mode should be used.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

#### JSON response

##### Returns:

* results: List[TimeMapResult] - The list of isochrone shapes.

##### Example:

```python
import asyncio

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.requests.time_map_fast import Transportation

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.time_map_fast_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        transportation=Transportation(type="driving+ferry"),
        travel_time=900
    )

    print(results)

asyncio.run(main())
```

#### GEOJSON response

##### Returns:

* results: FeatureCollection - The list of Features.

##### Example:

```python
import asyncio

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.requests.time_map_fast import Transportation

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.time_map_fast_geojson_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        transportation=Transportation(type="driving+ferry"),
        travel_time=900
    )

    print(results)

asyncio.run(main())
```

#### WKT response

##### Returns:

* results: TimeMapWKTResponse - TimeMapWktResponse with isochrone shapes.

##### Example:

```python
import asyncio

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.requests.time_map_fast import Transportation

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.time_map_fast_wkt_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        transportation=Transportation(type="driving+ferry"),
        travel_time=900
    )

    print(results)

asyncio.run(main())
```

#### WKT_NO_HOLES response

##### Returns:

* results: TimeMapWKTResponse - TimeMapWktResponse with isochrone shapes (no holes).

##### Example:

```python
import asyncio

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.requests.time_map_fast import Transportation

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.time_map_fast_wkt_no_holes_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        transportation=Transportation(type="driving+ferry"),
        travel_time=900
    )

    print(results)

asyncio.run(main())
```

### [Isochrones (H3)](https://docs.traveltime.com/api/reference/h3)

Calculate the travel times to all H3 cells within a travel time catchment area. Return the max, min, and mean travel time for each cell.

##### Takes:

* resolution: int - H3 resolution of results to be returned, values can be in range [1, 9].
* [properties](#cell-properties): List[CellProperty] - Properties to be returned for each H3 hexagon. Possible values: min, max, mean.
* coordinates: List[Union[Coordinates, H3Centroid]] - Coordinates of the departure location. Use either latitude and longitude, or the centroid of an h3 cell.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 3600
* [transportation](#transportation): Union - Transportation mode and related parameters.
* search_range: Range - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[H3Result] - The list of H3 isochrone cells.

##### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, H3Centroid
from traveltimepy.dto.transportation import Driving


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.h3_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        arrival_time=datetime.now(),
        transportation=Driving(),
        travel_time=900,
        resolution=8,
        properties=[CellProperty.MIN],
    )
    print(results)

asyncio.run(main())
```

### [H3 (Fast)](https://docs.traveltime.com/api/reference/h3-fast)

A very fast version of H3. However, the request parameters are more limited.

##### Takes:

* resolution: int - H3 resolution of results to be returned, values can be in range [1, 9].
* [properties](#cell-properties): List[CellProperty] - Properties to be returned for each H3 hexagon. Possible values: min, max, mean.
* coordinates: List[Union[Coordinates, H3Centroid]] - Coordinates of the departure location. Use either latitude and longitude, or the centroid of an h3 cell.
* [transportation]: Transportation - Transportation mode.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 10800. Default value is 3600.
* one_to_many: boolean - returns the reachable area for journeys arriving at the chosen arrival location if false,
returns the reachable area for journeys departing from the chosen departure location if true.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[H3Result] - The list of H3 isochrone cells.

##### Example:

```python
import asyncio

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, H3Centroid
from traveltimepy.dto.requests.time_filter_fast import Transportation

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.h3_fast_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        properties=[CellProperty.MIN],
        resolution = 8,
        transportation=Transportation(type="driving+ferry"),
        travel_time=900,
    )

    print(results)

asyncio.run(main())
```

### [Isochrones (Geohash)](https://docs.traveltime.com/api/reference/geohash)

Calculate the travel times to all geohash cells within a travel time catchment area. Return the max, min, and mean travel time for each cell.

##### Takes:

* resolution: int - H3 resolution of results to be returned, values can be in range [1, 6].
* [properties](#cell-properties): List[CellProperty] - Properties to be returned for each H3 hexagon. Possible values: min, max, mean.
* coordinates: List[Union[Coordinates, GeohashCentroid]] - Coordinates of the departure location. Use either latitude and longitude, or the centroid of a geohash cell.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 3600
* [transportation](#transportation): Union - Transportation mode and related parameters.
* search_range: Range - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[GeohashResult] - The list of H3 isochrone cells.

##### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, GeohashCentroid
from traveltimepy.dto.transportation import Driving


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.geohash_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            GeohashCentroid(geohash_centroid="gcpvj3"),
        ],
        arrival_time=datetime.now(),
        transportation=Driving(),
        travel_time=900,
        resolution=6,
        properties=[CellProperty.MIN],
    )
    print(results)

asyncio.run(main())
```

### [Geohash (Fast)](https://docs.traveltime.com/api/reference/geohash-fast)

A very fast version of Geohash. However, the request parameters are more limited.

##### Takes:

* resolution: int - Geohash resolution of results to be returned, values can be in range [1, 6].
* [properties](#cell-properties): List[CellProperty] - Properties to be returned for each Geohash hexagon. Possible values: min, max, mean.
* coordinates: List[Union[Coordinates, GeohashCentroid]] - Coordinates of the departure location. Use either latitude and longitude, or the centroid of a geohash cell.
* [transportation]: Transportation - Transportation mode.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 10800. Default value is 3600.
* one_to_many: boolean - returns the reachable area for journeys arriving at the chosen arrival location if false,
returns the reachable area for journeys departing from the chosen departure location if true.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[GeohashResult] - The list of geohash isochrone cells.

##### Example:

```python
import asyncio

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, GeohashCentroid
from traveltimepy.dto.requests.time_filter_fast import Transportation

async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.geohash_fast_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            GeohashCentroid(geohash_centroid="gcpvj3"),
        ],
        properties=[CellProperty.MIN],
        resolution = 6,
        transportation=Transportation(type="driving+ferry"),
        travel_time=900,
    )

    print(results)

asyncio.run(main())
```

### [Isochrone Intersections](https://docs.traveltime.com/api/reference/isochrones#intersections)

Given origin coordinates, find intersections of specified shapes or cells.

Currently these requests support Intersections in this SDK:
* [Time Map](#isochrones-time-map)
* [H3](#isochrones-h3)
* [Geohash](#isochrones-geohash)

##### Takes:

Intersection requests take the same params as their regular (`arrival_search` / `departure_search`) counterparts. Coordinates list size cannot be more than 10.

##### Returns:

Intersection requests return the same responses as their regular (`arrival_search` / `departure_search`) counterparts.

##### Examples:

**Time Map:**

```python
import asyncio
from datetime import datetime

from traveltimepy import Driving, Coordinates, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.time_map_intersection_async( # `sdk.intersection_async` will work too
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        arrival_time=datetime.now(),
        transportation=Driving()
    )

    print(results)


asyncio.run(main())
```

**H3:**

```python
import asyncio
from datetime import datetime

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, H3Centroid
from traveltimepy.dto.transportation import Driving


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.h3_intersection_async_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        arrival_time=datetime.now(),
        transportation=Driving(),
        travel_time=900,
        resolution=8,
        properties=[CellProperty.MIN],
    )
    print(results)

asyncio.run(main())
```

**Geohash:**

```python
import asyncio
from datetime import datetime

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, GeohashCentroid
from traveltimepy.dto.transportation import Driving


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.geohash_intersection_async_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            GeohashCentroid(geohash_centroid="gcpvj3"),
        ],
        arrival_time=datetime.now(),
        transportation=Driving(),
        travel_time=900,
        resolution=6,
        properties=[CellProperty.MIN],
    )
    print(results)

asyncio.run(main())
```

### [Isochrone Unions](https://docs.traveltime.com/api/reference/isochrones#unions)

Given origin coordinates, find unions of specified shapes or cells.

Currently these requests support Intersections in this SDK:
* [Time Map](#isochrones-time-map)
* [H3](#isochrones-h3)
* [Geohash](#isochrones-geohash)

##### Takes:

Union requests take the same params as their regular (`arrival_search` / `departure_search`) counterparts. Coordinates list size cannot be more than 10.

##### Returns:

Union requests return the same responses as their regular (`arrival_search` / `departure_search`) counterparts.

##### Examples:

**Time Map:**

```python
import asyncio
from datetime import datetime

from traveltimepy import Driving, Coordinates, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")
    results = await sdk.time_map_union_async( # `sdk.union_async` will work too
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.517609, lng=-0.138315)],
        arrival_time=datetime.now(),
        transportation=Driving()
    )

    print(results)


asyncio.run(main())
```

**H3:**

```python
import asyncio
from datetime import datetime

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, H3Centroid
from traveltimepy.dto.transportation import Driving


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.h3_union_async_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            H3Centroid(h3_centroid="87195da49ffffff"),
        ],
        arrival_time=datetime.now(),
        transportation=Driving(),
        travel_time=900,
        resolution=8,
        properties=[CellProperty.MIN],
    )
    print(results)

asyncio.run(main())
```

**Geohash:**

```python
import asyncio
from datetime import datetime

from traveltimepy import Coordinates, TravelTimeSdk
from traveltimepy.dto.common import CellProperty, GeohashCentroid
from traveltimepy.dto.transportation import Driving


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.geohash_union_async_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            GeohashCentroid(geohash_centroid="gcpvj3"),
        ],
        arrival_time=datetime.now(),
        transportation=Driving(),
        travel_time=900,
        resolution=6,
        properties=[CellProperty.MIN],
    )
    print(results)

asyncio.run(main())
```

### [Distance Map](https://docs.traveltime.com/api/reference/distance-map)

Given origin coordinates, find shapes of zones reachable within corresponding travel distance.

##### Takes:

* coordinates: List[Coordinates] - Coordinates of the arrival or departure location.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_distance: int - Maximum journey distance (in meters). Maximum value is 800000 (800km). Minimum value is 75. 
  Default value is 900.
* [transportation](#transportation): Union - Transportation mode and related parameters.
* [level_of_detail](#level-of-detail): LevelOfDetail - When enabled, allows the user to specify how detailed the isochrones should be.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* [no_holes](#no_holes): No holes - Enable to remove holes from returned polygons.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[TimeMapResult] - The list of isochrone shapes

##### Example:

```python
import asyncio
from datetime import datetime

from traveltimepy import Driving, Coordinates, TravelTimeSdk


async def main():
    sdk = TravelTimeSdk("YOUR_APP_ID", "YOUR_APP_KEY")

    results = await sdk.distance_map_async(
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

##### Takes:

* locations: List[Locations] - All locations. Location ids must be unique.
* search_ids: Dict[str, List[str]] - Search ids from a target location to destinations. You can define up to 2000
  destinations
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* [transportation](#transportation): Union - Transportation mode and related parameters.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 3600.
* properties: List[Property] - Properties to be returned about the points. Default value is travel_time.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.
* snapping: Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[TimeFilterResult] - The results list of reachable and unreachable locations.

##### Example:

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

A very fast version of `time_filter()`. However, the request parameters are much more limited.

##### Takes:

* locations: List[Locations] - All locations. Location ids must be unique.
* search_ids: Dict[str, List[str]] - Searches from a target location to destinations. You can define up to 100,000
  destinations
* [transportation]: Transportation - Transportation mode and related parameters.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 10800. Default value is 3600.
* properties: List[Property] - Properties to be returned about the points. Default value is travel_time.
* one_to_many: boolean - if one_to_many is equal to true, then it'll be a forward search (one to many matrix), false -
  backward search (many to one matrix). Default value is True.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[TimeFilterFastResult] - The results list of reachable and unreachable locations.

##### Example:

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

##### Takes:

* origin: Coordinates - Origin point.
* destinations: List[Coordinates] - Destination points. Cannot be more than 200,000.
* [transportation](#proto-transportation): Union[ProtoTransportation, PublicTransportWithDetails, DrivingAndPublicTransportWithDetails] - Transportation type with with optional extra details.
* travel_time: int - Time limit. Maximum value is 7200.
* country: ProtoCountry - Return the results that are within the specified country.
* one_to_many: boolean - if one_to_many is equal to true, then it'll be a forward search (one to many matrix), false -
  backward search (many to one matrix). Default value is True.
* properties: List[PropertyProto] - specifies which extra properties should be calculated in the response. 

##### Returns:

* results: TimeFilterProtoResponse - The response contains:
  * list of travel times, where each position denotes either a travel time (in seconds)
    of a journey, or if travel time is negative, that the journey from the origin to the destination point is impossible. 
  * (optional) list of distances where each position denotes distance (in meters) to the specified location. 
##### Example:

```python
import asyncio
from traveltimepy import ProtoCountry, Coordinates, ProtoTransportation, TravelTimeSdk, PropertyProto

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
        country=ProtoCountry.UNITED_KINGDOM,
        properties=[PropertyProto.DISTANCE],
    )
    
    print(travel_times)

asyncio.run(main())
```

### [Routes](https://docs.traveltime.com/api/reference/routes)

Returns routing information between source and destinations.

##### Takes:

* locations: List[Locations] - All locations. Location ids must be unique.
* search_ids: Dict[str, List[str]] - Searches from a target location to destinations.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* [transportation](#transportation): Union - Transportation mode and related parameters.
* properties: List[Property] - Properties to be returned about the locations. Default value is travel_time.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.
* [snapping](#snapping): Snapping - Adjusts the process of looking up the nearest roads from the departure / arrival points.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[RoutesResult] - The results list of routes.

##### Example:

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

##### Takes:

* query: str - A query to geocode. Can be an address, a postcode or a venue.
* within_countries: List[str] - Only return the results that are within the specified country.
* limit: int - Expected integer between 1 and 50. Limits amount of results returned to specified number.
* format_name: bool - Format the name field of the geocoding search response to a well formatted, human-readable address
  of the location.
* format_exclude_country: bool - Exclude the country from the formatted name field.
* bounds: Rectangle - Used to limit the results to a bounding box.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* Matched locations in geojson format

##### Example:

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

##### Takes:

* lat: float - Latitude
* lng: float - Longitude
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* Matched locations in a geojson format

##### Example:

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

##### Takes:

* coordinates: List[Coordinates] - Location coordinates.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 1800
* [transportation](#transportation): Union - Transportation mode and related parameters.
* properties: List[Property] - Properties to be returned about the postcodes. Default value is travel_time.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[PostcodesResult] - The results list of postcodes.

##### Example:

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

##### Takes:

* coordinates: List[Coordinates] - Location coordinates.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 1800
* [transportation](#transportation): Union - Transportation mode and related parameters.
* reachable_postcodes_threshold: float - A number between 0.0 and 1.0. Default value is 0.1. For example, if 0.5 is
  used, only districts that have at least 50% postcodes that can be reached within the given travel_time will be
  included in the response. 0 will return districts that have at least a single reachable postcode.
* properties: List[Property] - Properties to be returned about the districts. Default value is travel_time_all.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[DistrictsResult] - The results list of districts.

##### Example:

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

##### Takes:

* coordinates: List[Coordinates] - Location coordinates.
* arrival_time: datetime - Be at arrival location at no later than given time. Cannot be specified with departure_time.
* departure_time: datetime - Leave departure location at no earlier than given time. Cannot be specified with
  arrival_time.
* travel_time: int - Maximum journey time (in seconds). Maximum value is 14400. Default value is 1800
* [transportation](#transportation): Union - Transportation mode and related parameters.
* reachable_postcodes_threshold: float - A number between 0.0 and 1.0. Default value is 0.1. For example, if 0.5 is
  used, only sectors that have at least 50% postcodes that can be reached within the given travel_time will be included
  in the response. 0 will return sectors that have at least a single reachable postcode.
* properties: List[Property] - Properties to be returned about the sectors. Default value is travel_time_all.
* range: FullRange - When enabled, range adds an arrival window to the arrival time, and results are returned for any
  journeys that arrive during this window.
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* results: List[SectorsResult] - The results list of postcode sectors.

##### Example:

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

##### Returns:

* maps: List[Map]
* name - An internal map id. The first two characters usually correspond to the ISO 3166-2 standard (e.g th, ie)
  sometimes followed by additional characters (e.g ca_pst, us_pst). To get features of a specific map, use the map
  info endpoint.
* features - Features that are supported in the specified map
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Example:

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

##### Takes:

* locations: List[Location] - Each location requires an id and lat/lng values
* v4_endpoint_path: str - If defined, overrides the endpoint of the url `f"/v4/{v4_endpoint_path}"`.

##### Returns:

* locations: List[SupportedLocation]
* id - Location id that you specified in the request.
* map_name - An internal map id. The first two characters usually correspond to the ISO 3166-2 standard (e.g th, ie)
  sometimes followed by additional characters (e.g ca_pst, us_pst). To get features of a specific map, use the map
  info endpoint.
* additional_map_names - In case the location is in more than one map, other map ids are listed here.
* unsupported_locations: List[str] - List that contains ids of locations that are unsupported.

##### Example:

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

## Parameter usage examples

### Transportation

In [transportation.py](https://github.com/traveltime-dev/traveltime-python-sdk/blob/master/traveltimepy/dto/transportation.py)
you can find all implemented transportation types, their sub-parameters and their default values.

These examples don't apply to proto / fast endpoints. For more examples you can always refer to [Unit Tests](https://github.com/traveltime-dev/traveltime-python-sdk/tree/master/tests)

#### Driving 

```python
from traveltimepy import Driving, DrivingTrafficModel

transportation=Driving()
transportation=Driving(disable_border_crossing = True)
transportation=Driving(traffic_model = DrivingTrafficModel.OPTIMISTIC)
```

#### Walking 

```python
from traveltimepy import Walking 

transportation=Walking()
```

#### Cycling 

```python
from traveltimepy import Cycling 

transportation=Cycling()
```

#### Ferry 

```python
from traveltimepy import Ferry, DrivingTrafficModel

transportation=Ferry()
transportation=Ferry(type="cycling+ferry")
transportation=Ferry(type="driving+ferry")
transportation=Ferry(type="cycling+ferry", boarding_time = 300)

transportation=Ferry(type="driving+ferry", traffic_model=DrivingTrafficModel.OPTIMISTIC)
```

#### DrivingTrain 

```python
from traveltimepy import DrivingTrain, MaxChanges, DrivingTrafficModel

transportation=DrivingTrain()

transportation=DrivingTrain(
  pt_change_delay = 300, 
  driving_time_to_station=1800, 
  parking_time=800,
  walking_time=500,
  max_changes=MaxChanges(enabled=True, limit=3),
  traffic_model=DrivingTrafficModel.OPTIMISTIC
)
```

#### PublicTransport 

```python
from traveltimepy import PublicTransport, MaxChanges

transportation=PublicTransport() # type="public_transport" - any public transport
transportation=PublicTransport(type="train")
transportation=PublicTransport(type="bus")
transportation=PublicTransport(type="coach")

transportation=PublicTransport(
  pt_change_delay = 300, 
  walking_time=500,
  max_changes=MaxChanges(enabled=True, limit=3)
)
```

#### CyclingPublicTransport 

```python
from traveltimepy import CyclingPublicTransport, MaxChanges

transportation=CyclingPublicTransport()

transportation=CyclingPublicTransport(
  walking_time=500,
  pt_change_delay = 300,
  cycling_time_to_station=300,
  parking_time=800,
  boarding_time=300,
  max_changes=MaxChanges(enabled=True, limit=3)
)
```

### Proto Transportation

When picking transportation mode for proto requests take note that some of the transportation modes
support extra configuration parameters.

* transportation: Union[ProtoTransportation, PublicTransportWithDetails, DrivingAndPublicTransportWithDetails]

Examples:

#### ProtoTransportation

Select transportation mode, no extra parameters

```python
from traveltimepy.dto.requests.time_filter_proto import ProtoTransportation

transportation=ProtoTransportation.PUBLIC_TRANSPORT

transportation=ProtoTransportation.DRIVING 

transportation=ProtoTransportation.DRIVING_AND_PUBLIC_TRANSPORT 

transportation=ProtoTransportation.DRIVING_FERRY 

transportation=ProtoTransportation.WALKING 

transportation=ProtoTransportation.CYCLING 

transportation=ProtoTransportation.CYCLING_FERRY 

transportation=ProtoTransportation.WALKING_FERRY 
```

#### PublicTransportWithDetails

This mode uses `ProtoTransportation.PUBLIC_TRANSPORT` transportion mode and allows to set these parameters:
* `walking_time_to_station` - limits the possible duration of walking paths.
  This limit is of low precedence and will not override the global travel time limit
  Optional. Must be <= 1800.

```python
from traveltimepy.dto.requests.time_filter_proto import PublicTransportWithDetails

transportation=PublicTransportWithDetails()

transportation=PublicTransportWithDetails(walking_time_to_station=900)
```

#### DrivingAndPublicTransportWithDetails

This mode uses `ProtoTransportation.DRIVING_AND_PUBLIC_TRANSPORT` transportion mode and allows to set these parameters:
* `walking_time_to_station` - limits the possible duration of walking paths.
  This limit is of low precedence and will not override the global travel time limit.
  Optional. Must be <= 1800.
* `driving_time_to_station` - limits the possible duration of driving paths.
  This limit is of low precedence and will not override the global travel time limit
  Optional. Must be <= 1800.
* `parking_time` - constant penalty to apply to simulate the difficulty of finding a parking spot.
  Optional. Cannot be greater than the global travel time limit.

```python
from traveltimepy.dto.requests.time_filter_proto import DrivingAndPublicTransportWithDetails

transportation=DrivingAndPublicTransportWithDetails()

transportation=DrivingAndPublicTransportWithDetails(walking_time_to_station=900, driving_time_to_station=1800, parking_time=300)
```

### Level of Detail

`level_of_detail` can be used to specify how detailed the isochrone result should be.

For a more detailed description of how to use this parameter, you can refer to our [API Docs](https://docs.traveltime.com/api/reference/isochrones#arrival_searches-level_of_detail)

#### Examples

```python
from traveltimepy import LevelOfDetail

# scale_type "simple"
level_of_detail=LevelOfDetail(scale_type="simple", level="lowest")

# scale_type "simple_numeric"
level_of_detail=LevelOfDetail(scale_type="simple_numeric", level=0)

# scale_type "coarse_grid"
level_of_detail=LevelOfDetail(scale_type="coarse_grid", square_size=600)
```

### Snapping

`snapping` Adjusts the process of looking up the nearest roads from the departure / arrival points.

For a more detailed description of how to use this parameter, you can refer to our [API Docs](https://docs.traveltime.com/api/reference/isochrones#departure_searches-snapping)

#### Examples

```python
from traveltimepy.dto.common import Snapping, SnappingAcceptRoads, SnappingPenalty

snapping=Snapping(
    penalty=SnappingPenalty.ENABLED, # default
    accept_roads=SnappingAcceptRoads.BOTH_DRIVABLE_AND_WALKABLE # default
)

snapping=Snapping(
    penalty=SnappingPenalty.DISABLED,
    accept_roads=SnappingAcceptRoads.ANY_DRIVABLE
)
```

### Cell Properties

Cell properties are the `properties` param used in H3 and geohash requests. Specifies proprties to be returned for each cell. Possible values: min, max, mean.

#### Examples

```python
from traveltimepy.dto.common import CellProperty

# all properties
properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN]

# some properties
properties=[CellProperty.MIN]
```

### Polygons Filter

`polygons_filter` specifies polygon filter of a single shape.

For a more detailed description of how to use this parameter, you can refer to our [API Docs](https://docs.traveltime.com/api/reference/isochrones#departure_searches-polygons_filter)

#### Examples

```python
from traveltimepy.dto.common import PolygonsFilter

polygons_filter = PolygonsFilter(limit=1)
polygons_filter = PolygonsFilter(limit=5)
```

### Render Mode

`render_mode` specifies how the shape should be rendered.

For a more detailed description of how to use this parameter, you can refer to our [API Docs](https://docs.traveltime.com/api/reference/isochrones#departure_searches-render_mode)

#### Examples

```python
from traveltimepy.dto.common import RenderMode

render_mode = RenderMode.APPROXIMATE_TIME_FILTER  # default
render_mode = RenderMode.ROAD_BUFFERING
```
