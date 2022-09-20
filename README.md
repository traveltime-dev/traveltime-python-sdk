# traveltimePY: Travel Time Python SDK

traveltimePY is a Python SDK for Travel Time API (https://traveltime.com/).  
Travel Time API helps users find locations by journey time rather than using ‘as the crow flies’ distance.  
Time-based searching gives users more opportunities for personalisation and delivers a more relevant search.

Dependencies:

* requests

## Installation

```python
    pip install traveltimepy
```

## Usage

### Authentication
In order to authenticate with Travel Time API, you will have to supply the Application Id and Api Key. 

```python
    import traveltimepy as ttpy
    import os
    from datetime import datetime #for examples
    #store your credentials in an environment variable
    os.environ["TRAVELTIME_ID"] = 'YOUR_API_ID'
    os.environ["TRAVELTIME_KEY"] = 'YOUR_API_KEY'
```

### [Isochrones (Time Map)](https://traveltime.com/docs/api/reference/isochrones)
Given origin coordinates, find shapes of zones reachable within corresponding travel time.

```python
    departure_search1 = {
        'id': "public transport from Trafalgar Square",
        'departure_time':  datetime.utcnow().isoformat(),
        'travel_time': 900,
        'coords': {'lat': 51.507609, 'lng': -0.128315},
        'transportation': {'type': "public_transport"},
        'properties': ['is_only_walking']
    }
    departure_search2 = {
        'id': "driving from Trafalgar Square",
        'departure_time':  datetime.utcnow().isoformat(),
        'travel_time': 900,
        'coords': {'lat': 51.507609, 'lng': -0.128315},
        'transportation': {'type': "driving"}
    }
    arrival_search = {
        'id': "public transport to Trafalgar Square",
        'arrival_time':  datetime.utcnow().isoformat(),
        'travel_time': 900,
        'coords': {'lat': 51.507609, 'lng': -0.128315},
        'transportation': {'type': "public_transport"},
        'range': {'enabled': True, 'width': 3600}
    }
    union = {
        'id': "union of driving and public transport",
        'search_ids': ['driving from Trafalgar Square', 'public transport from Trafalgar Square']
    }
    intersection = {
        'id': "intersection of driving and public transport",
        'search_ids': ['driving from Trafalgar Square', 'public transport from Trafalgar Square']
    }
    out = ttpy.time_map(departure_searches=[departure_search1, departure_search2],
                            arrival_searches=arrival_search, unions=union, intersections=intersection)
```

### [Distance Matrix (Time Filter)](https://traveltime.com/docs/api/reference/distance-matrix)
Given origin and destination points filter out points that cannot be reached within specified time limit.

```python
    locations = [
        {"id": "London center", "coords": {"lat": 51.508930, "lng": -0.131387}},
        {"id": "Hyde Park", "coords": {"lat": 51.508824, "lng": -0.167093}},
        {"id": "ZSL London Zoo", "coords": {"lat": 51.536067, "lng": -0.153596}}
    ]

    departure_search = {
        "id": "forward search example",
        "departure_location_id": "London center",
        "arrival_location_ids": ["Hyde Park", "ZSL London Zoo"],
        "transportation": {"type": "bus"},
        "departure_time":  datetime.utcnow().isoformat(),
        "travel_time": 1800,
        "properties": ["travel_time"],
        "range": {"enabled": True, "max_results": 3, "width": 600}
    }

    arrival_search = {
        "id": "backward search example",
        "departure_location_ids": ["Hyde Park", "ZSL London Zoo"],
        "arrival_location_id": "London center",
        "transportation": {"type": "public_transport"},
        "arrival_time":  datetime.utcnow().isoformat(),
        "travel_time": 1900,
        "properties": ["travel_time", "distance", "distance_breakdown", "fares"]
    }

    out = ttpy.time_filter(
        locations=locations, departure_searches=departure_search, arrival_searches=arrival_search)
```

### [Routes](https://traveltime.com/docs/api/reference/routes)
Returns routing information between source and destinations.

```python
    locations = [
        {"id": "London center", "coords": {"lat": 51.508930, "lng": -0.131387}},
        {"id": "Hyde Park", "coords": {"lat": 51.508824, "lng": -0.167093}},
        {"id": "ZSL London Zoo", "coords": {"lat": 51.536067, "lng": -0.153596}}
    ]

    departure_search = {
        "id": "departure search example",
        "departure_location_id": "London center",
        "arrival_location_ids": ["Hyde Park", "ZSL London Zoo"],
        "transportation": {"type": "driving"},
        "departure_time":  datetime.utcnow().isoformat(),
        "properties": ["travel_time", "distance", "route"]
    }

    arrival_search = {
        "id": "arrival  search example",
        "departure_location_ids": ["Hyde Park", "ZSL London Zoo"],
        "arrival_location_id": "London center",
        "transportation": {"type": "public_transport"},
        "arrival_time":  datetime.utcnow().isoformat(),
        "properties": ["travel_time", "distance", "route", "fares"],
        "range": {"enabled": True, "max_results": 1, "width": 1800}
    }

    out = ttpy.routes(
        locations=locations, departure_searches=departure_search, arrival_searches=arrival_search)
```

### [Time Filter (Fast)](https://traveltime.com/docs/api/reference/time-filter-fast)
A very fast version of ``time_filter()``

```python
    locations = [
        {"id": "London center", "coords": {"lat": 51.508930, "lng": -0.131387}},
        {"id": "Hyde Park", "coords": {"lat": 51.508824, "lng": -0.167093}},
        {"id": "ZSL London Zoo", "coords": {"lat": 51.536067, "lng": -0.153596}}
    ]

    arrival_many_to_one = {
    "id": "arrive-at many-to-one search example",
    "departure_location_ids": ["Hyde Park","ZSL London Zoo"],
    "arrival_location_id": "London center",
    "transportation": {"type": "public_transport"},
    "arrival_time_period": "weekday_morning",
    "travel_time": 1900,
    "properties": ["travel_time","fares"]
    }
    arrival_one_to_many = {
    "id": "arrive-at one-to-many search example",
    "arrival_location_ids": ["Hyde Park","ZSL London Zoo"],
    "departure_location_id": "London center",
    "transportation": {"type": "public_transport"},
    "arrival_time_period": "weekday_morning",
    "travel_time": 1900,
    "properties": ["travel_time","fares"]
    }

    out = ttpy.time_filter_fast(
        locations=locations, arrival_many_to_one=arrival_many_to_one, arrival_one_to_many=arrival_one_to_many)
```

### [Time Filter (Postcode Districts)](https://traveltime.com/docs/api/reference/postcode-district-filter)
Find reachable postcodes from origin (or to destination) and get statistics about such postcodes.

```python
    departure_search = {
        'id': "public transport from Trafalgar Square",
        'departure_time':  datetime.utcnow().isoformat(),
        'travel_time': 1800,
        'coords': {'lat': 51.507609, 'lng': -0.128315},
        'transportation': {'type': "public_transport"},
        'properties': ["coverage", "travel_time_reachable", "travel_time_all"],
        "reachable_postcodes_threshold": 0.1
    }
    arrival_search = {
        'id': "public transport to Trafalgar Square",
        'arrival_time':  datetime.utcnow().isoformat(),
        'travel_time': 1800,
        'coords': {'lat': 51.507609, 'lng': -0.128315},
        'transportation': {'type': "public_transport"},
        'properties': ["coverage", "travel_time_reachable", "travel_time_all"],
        "reachable_postcodes_threshold": 0.1
    }
    out = ttpy.time_filter_postcode_districts(departure_searches=departure_search, arrival_searches=arrival_search)
```

### [Time Filter (Postcode Sectors)](https://traveltime.com/docs/api/reference/postcode-sector-filter)
Find sectors that have a certain coverage from origin (or to destination) and get statistics about postcodes within such sectors.

```python
    departure_search = {
        'id': "public transport from Trafalgar Square",
        'departure_time':  datetime.utcnow().isoformat(),
        'travel_time': 1800,
        'coords': {'lat': 51.507609, 'lng': -0.128315},
        'transportation': {'type': "public_transport"},
        'properties': ["coverage", "travel_time_reachable", "travel_time_all"],
        "reachable_postcodes_threshold": 0.1
    }
    arrival_search = {
        'id': "public transport to Trafalgar Square",
        'arrival_time':  datetime.utcnow().isoformat(),
        'travel_time': 1800,
        'coords': {'lat': 51.507609, 'lng': -0.128315},
        'transportation': {'type': "public_transport"},
        'properties': ["coverage", "travel_time_reachable", "travel_time_all"],
        "reachable_postcodes_threshold": 0.1
    }
    out = ttpy.time_filter_postcode_sectors(departure_searches=departure_search, arrival_searches=arrival_search)
```

### [Time Filter (Postcodes)](https://traveltime.com/docs/api/reference/postcode-search)
Find reachable postcodes from origin (or to destination) and get statistics about such postcodes.

```python
    departure_search = {
        'id': "public transport from Trafalgar Square",
        'departure_time':  datetime.utcnow().isoformat(),
        'travel_time': 1800,
        'coords': {'lat': 51.507609, 'lng': -0.128315},
        'transportation': {'type': "public_transport"},
        'properties': ["travel_time", "distance"]
    }
    arrival_search = {
        'id': "public transport to Trafalgar Square",
        'arrival_time':  datetime.utcnow().isoformat(),
        'travel_time': 1800,
        'coords': {'lat': 51.507609, 'lng': -0.128315},
        'transportation': {'type': "public_transport"},
        'properties': ["travel_time", "distance"]
    }
    out = ttpy.time_filter_postcodes(departure_searches=departure_search, arrival_searches=arrival_search)
```

### [Geocoding (Search)](https://traveltime.com/docs/api/reference/geocoding-search) and [Reverse Geocoding](https://traveltime.com/docs/api/reference/geocoding-reverse)
Match a query string to geographic coordinates or match a latitude, longitude pair to an address.

```python
    out1 = ttpy.geocoding('Parliament square')
    out2 = ttpy.geocoding_reverse(lat=51.507281, lng=-0.132120)
```

### [Map Info](https://traveltime.com/docs/api/reference/map-info) and [Supported Locations](https://traveltime.com/docs/api/reference/supported-locations)
Get information about currently supported countries and find out what points are supported by the api.

```python
    out1 = ttpy.map_info()
    locations = [
        {"id": "Kaunas", "coords": {"lat": 54.900008, "lng": 23.957734}},
        {"id": "London", "coords": {"lat": 51.506756, "lng": -0.128050}},
        {"id": "Bangkok", "coords": {"lat": 13.761866, "lng": 100.544818}},
        {"id": "Lisbon", "coords": {"lat": 38.721869, "lng": -9.138549}}
    ]
    out2 = ttpy.supported_locations(locations=locations)
```
