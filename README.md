# TravelTime Python SDK

[![PyPI version](https://badge.fury.io/py/traveltimepy.svg)](https://badge.fury.io/py/traveltimepy)
[![Unit Tests](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/traveltime-dev/traveltime-python-sdk/actions/workflows/ci.yml)
[![Python support](https://img.shields.io/badge/python-3.9+-blue.svg)](https://img.shields.io/badge/python-3.9+-blue)

The TravelTime Python SDK provides a simple and efficient way to access the [TravelTime API](https://docs.traveltime.com/api/overview/introduction), enabling you to calculate travel times and distances, generate isochrones, and perform location-based queries using real-world transportation data.

## Features

- **Time Matrix & Filtering**: Calculate travel times between multiple origins and destinations
- **Isochrone Generation**: Create time-based catchment areas in multiple formats (GeoJSON, WKT)
- **Route Planning**: Get detailed turn-by-turn directions between locations
- **Geocoding**: Convert addresses to coordinates and vice versa
- **Specialized Analysis**: UK postcode analysis, H3 hexagon analysis, and geohash analysis
- **Transportation Modes**: Support for driving, public transport, walking, cycling, and multimodal transport
- **Async Support**: Both synchronous and asynchronous clients available
- **Performance Options**: Fast endpoints for high-volume use cases

## Requirements

- Python 3.9 or higher

To check your Python version:
```bash
python --version
```

## Installation

Install the TravelTime Python SDK using pip:

```bash
pip install traveltimepy
```

## Getting Started

### Authentication

Get your API credentials from the [TravelTime Developer Portal](https://docs.traveltime.com/api/overview/getting-keys).

### Basic Usage

```python
from datetime import datetime
from traveltimepy import Client
from traveltimepy.requests.common import Location, Coordinates, Property
from traveltimepy.requests.time_filter import TimeFilterDepartureSearch
from traveltimepy.requests.transportation import PublicTransport
from traveltimepy.errors import TravelTimeApiError

# Define locations
locations = [
    Location(id="London center", coords=Coordinates(lat=51.508930, lng=-0.131387)),
    Location(id="Hyde Park", coords=Coordinates(lat=51.508824, lng=-0.167093)),
    Location(id="ZSL London Zoo", coords=Coordinates(lat=51.536067, lng=-0.153596))
]

# Option 1: Standard usage (manual session management)
client = Client(app_id="YOUR_APP_ID", api_key="YOUR_API_KEY")

try:
    response = client.time_filter(
        locations=locations,
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center", 
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,  # 30 minutes
                properties=[Property.TRAVEL_TIME]
            )
        ],
        arrival_searches=[]
    )
    
    print(f"Found {len(response.results)} results")
    for result in response.results:
        print(f"Search ID: {result.search_id}")
            
except TravelTimeApiError as e:
    print(e)
finally:
    client.close()  # Manually close session

# Option 2: Context manager (automatic session cleanup)
with Client(app_id="YOUR_APP_ID", api_key="YOUR_API_KEY") as client:
    try:
        response = client.time_filter(
            locations=locations,
            departure_searches=[
                TimeFilterDepartureSearch(
                    id="London center",
                    departure_location_id="London center", 
                    arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                    departure_time=datetime.now(),
                    transportation=PublicTransport(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME]
                )
            ],
            arrival_searches=[]
        )
        
        print(f"Found {len(response.results)} results")
        for result in response.results:
            print(f"Search ID: {result.search_id}")
            
    except TravelTimeApiError as e:
        print(e)
    # Session automatically closed when exiting 'with' block
```

### Async Usage

```python
import asyncio
from datetime import datetime
from traveltimepy import AsyncClient
from traveltimepy.requests.common import Location, Coordinates
from traveltimepy.requests.time_filter import TimeFilterDepartureSearch
from traveltimepy.requests.transportation import PublicTransport
from traveltimepy.errors import TravelTimeApiError

locations = [
    Location(id="London center", coords=Coordinates(lat=51.508930, lng=-0.131387)),
    Location(id="Hyde Park", coords=Coordinates(lat=51.508824, lng=-0.167093)),
    Location(id="ZSL London Zoo", coords=Coordinates(lat=51.536067, lng=-0.153596))
]

# Option 1: Standard async usage (manual session management)
async def main():
    client = AsyncClient(app_id="YOUR_APP_ID", api_key="YOUR_API_KEY")
    
    try:
        response = await client.time_filter(
            locations=locations,
            departure_searches=[
                TimeFilterDepartureSearch(
                    id="London center",
                    departure_location_id="London center",
                    arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                    departure_time=datetime.now(),
                    transportation=PublicTransport(),
                    travel_time=1800
                )
            ],
            arrival_searches=[]
        )
        
        print(f"Found {len(response.results)} results")
        for result in response.results:
            print(f"Search ID: {result.search_id}")
            
    except TravelTimeApiError as e:
        print(e)
    finally:
        await client.close()  # Manually close session

# Option 2: Async context manager (automatic session cleanup)
async def main_with_context():
    async with AsyncClient(app_id="YOUR_APP_ID", api_key="YOUR_API_KEY") as client:
        try:
            response = await client.time_filter(
                locations=locations,
                departure_searches=[
                    TimeFilterDepartureSearch(
                        id="London center",
                        departure_location_id="London center",
                        arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                        departure_time=datetime.now(),
                        transportation=PublicTransport(),
                        travel_time=1800
                    )
                ],
                arrival_searches=[]
            )
            
            print(f"Found {len(response.results)} results")
            for result in response.results:
                print(f"Search ID: {result.search_id}")
                
        except TravelTimeApiError as e:
            print(e)
        # Session automatically closed when exiting 'async with' block

# Run either version
asyncio.run(main())
# or
asyncio.run(main_with_context())
```

## Core Methods

The SDK provides both synchronous (`Client`) and asynchronous (`AsyncClient`) versions of all methods:

### Time Matrix & Filtering

- [`time_filter()`](https://docs.traveltime.com/api/reference/travel-time-distance-matrix) - Calculate travel times between locations
- [`time_filter_fast()`](https://docs.traveltime.com/api/reference/time-filter-fast) - High-performance version for large datasets
- [`time_filter_proto()`](https://docs.traveltime.com/api/start/travel-time-distance-matrix-proto) - Ultra-fast protocol buffer implementation

### Isochrone Generation

- [`time_map()`](https://docs.traveltime.com/api/reference/isochrones) - Generate travel time polygons
- [`time_map_geojson()`](https://docs.traveltime.com/api/reference/isochrones) - GeoJSON format isochrones
- [`time_map_wkt()`](https://docs.traveltime.com/api/reference/isochrones) - WKT format isochrones
- [`time_map_fast()`](https://docs.traveltime.com/api/reference/isochrones-fast) - High-performance isochrones
- [`time_map_fast_geojson()`](https://docs.traveltime.com/api/reference/isochrones-fast) - Fast GeoJSON isochrones
- [`time_map_fast_wkt()`](https://docs.traveltime.com/api/reference/isochrones-fast) - Fast WKT isochrones

### Route Planning

- [`routes()`](https://docs.traveltime.com/api/reference/routes) - Calculate detailed routes between locations

### Geocoding

- [`geocoding()`](https://docs.traveltime.com/api/reference/geocoding-search) - Convert addresses to coordinates
- [`reverse_geocoding()`](https://docs.traveltime.com/api/reference/geocoding-reverse) - Convert coordinates to addresses

### Specialized Analysis

- [`h3()`](https://docs.traveltime.com/api/reference/h3) - H3 hexagon analysis
- [`h3_fast()`](https://docs.traveltime.com/api/reference/h3-fast) - Fast H3 analysis
- [`geohash()`](https://docs.traveltime.com/api/reference/geohash) - Geohash analysis
- [`geohash_fast()`](https://docs.traveltime.com/api/reference/geohash-fast) - Fast geohash analysis
- [`postcodes()`](https://docs.traveltime.com/api/reference/postcode-search) - UK postcode analysis
- [`postcode_districts()`](https://docs.traveltime.com/api/reference/postcode-district-filter) - UK postcode district analysis
- [`postcode_sectors()`](https://docs.traveltime.com/api/reference/postcode-sector-filter) - UK postcode sector analysis
- [`distance_map()`](https://docs.traveltime.com/api/reference/distance-map) - Distance-based catchment areas

### Utility Methods

- [`map_info()`](https://docs.traveltime.com/api/reference/map-info) - Get supported countries and features
- [`supported_locations()`](https://docs.traveltime.com/api/reference/supported-locations) - Check location support

## Configuration

The SDK supports various configuration options:

```python
from traveltimepy import Client, AsyncClient

# Synchronous client
client = Client(
    app_id="YOUR_APP_ID",
    api_key="YOUR_API_KEY",
    timeout=300,                    # Request timeout in seconds
    retry_attempts=3,               # Number of retry attempts for 5xx errors
    max_rpm=60,                     # Maximum requests per minute
)

# Asynchronous client
async_client = AsyncClient(
    app_id="YOUR_APP_ID",
    api_key="YOUR_API_KEY",
    timeout=300,
    retry_attempts=3,
    max_rpm=60
)
```


## Error Handling and Retries

The SDK automatically handles both rate limiting and server error retries:

- **Rate limiting**: Automatically handled with exponential backoff
- **Server errors (5xx)**: Automatically retried up to 3 times with immediate retry
- **Client errors (4xx)**: Not retried (indicates invalid request)

```python
# Retries are built-in - no additional code needed
client = Client(app_id="YOUR_APP_ID", api_key="YOUR_API_KEY")
response = client.time_filter(
    locations=locations,
    departure_searches=searches
)  # Automatically retries on 5xx errors
```

### Configuring Retries

You can configure the number of retry attempts:

```python
# Custom retry attempts
client = Client(
    app_id="YOUR_APP_ID", 
    api_key="YOUR_API_KEY",
    retry_attempts=5  # Will retry up to 5 times on 5xx errors
)

# Disable retries completely
client = Client(
    app_id="YOUR_APP_ID", 
    api_key="YOUR_API_KEY",
    retry_attempts=0  # No retries, fail immediately
)
```

## Examples

The `examples/` directory contains practical examples.
See [examples/README.md](examples/README.md) for setup instructions and detailed descriptions.

## Performance Tips

- Use `*_fast()` methods for high-volume use cases
- Use `time_filter_proto()` for maximum performance with large datasets
- Use async methods for I/O-bound applications

## Documentation

For comprehensive documentation, including detailed parameter references and advanced usage examples, visit:

- [TravelTime API Documentation](https://docs.traveltime.com/api/overview/introduction)

## Support

If you have questions or need help:

- [Create an issue](https://github.com/traveltime-dev/traveltime-python-sdk/issues) on GitHub
- Check the [API documentation](https://docs.traveltime.com/)
- Contact [TravelTime support](https://traveltime.com/contact-us)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
