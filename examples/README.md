# TravelTime Python SDK Examples

This directory contains examples demonstrating how to use the TravelTime Python SDK for real-world use cases.

## Setup

Before running the examples, you need to:

1. Install dependencies:
   ```bash
   pip install -r examples/requirements.txt
   ```

2. Set your API credentials as environment variables:
   ```bash
   export TRAVELTIME_APP_ID="your_app_id"
   export TRAVELTIME_API_KEY="your_api_key"
   ```
   Get your API credentials from [TravelTime API Dashboard](https://docs.traveltime.com/api/overview/getting-keys)

## Examples

### time_filter.py - Public Transport Accessibility Analysis  
Check if essential services are reachable within 1 hour by public transport from different residential areas in London. Demonstrates concurrent API calls using AsyncClient.

```bash
python examples/time_filter.py
```

### time_filter_fast_proto.py - High-Performance Shop Finder
Find the 3 closest shops by driving time using the Protocol Buffers API for maximum performance. Shows one-to-many distance matrix calculation.

```bash
python examples/time_filter_fast_proto.py
```

### geocoding.py - London Walking Tour Planner
Plan a walking tour of famous London landmarks. Uses geocoding to get coordinates, then calculates total walking time including 30-minute stops at each location.

```bash
python examples/geocoding.py
```

## Running Examples

Each example can be run directly from the project root:

```bash
PYTHONPATH=. python examples/time_filter.py
PYTHONPATH=. python examples/time_filter_fast_proto.py
PYTHONPATH=. python examples/geocoding.py
```

## Dependencies

- `traveltimepy` - TravelTime Python SDK