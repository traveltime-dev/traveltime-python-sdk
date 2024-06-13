from typing import List

import pytest
from datetime import datetime

from traveltimepy import PublicTransport, Driving, Location, Coordinates
from traveltimepy.dto.common import Snapping, SnappingAcceptRoads, SnappingPenalty
from traveltimepy.sdk import TravelTimeSdk


@pytest.mark.asyncio
async def test_departures(sdk: TravelTimeSdk, locations):
    results = await sdk.routes_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now(),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals(sdk: TravelTimeSdk, locations):
    results = await sdk.routes_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now(),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_snapping(sdk: TravelTimeSdk):
    locations: List[Location] = [
        Location(id="A", coords=Coordinates(lat=53.806479, lng=-2.615711)),
        Location(id="B", coords=Coordinates(lat=53.810129, lng=-2.601099)),
    ]
    result_with_penalty = await sdk.routes_async(
        locations=locations,
        search_ids={
            "A": ["B"],
        },
        transportation=Driving(),
        departure_time=datetime.now(),
    )
    traveltime_with_penalty = (
        result_with_penalty[0].locations[0].properties[0].travel_time
    )
    result_without_penalty = await sdk.routes_async(
        locations=locations,
        search_ids={
            "A": ["B"],
        },
        transportation=Driving(),
        departure_time=datetime.now(),
        snapping=Snapping(
            penalty=SnappingPenalty.DISABLED,
            accept_roads=SnappingAcceptRoads.ANY_DRIVABLE,
        ),
    )
    traveltime_without_penalty = (
        result_without_penalty[0].locations[0].properties[0].travel_time
    )
    assert traveltime_with_penalty is not None
    assert traveltime_without_penalty is not None
    assert traveltime_with_penalty > traveltime_without_penalty
