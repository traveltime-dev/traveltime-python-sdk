from datetime import datetime
from typing import List

import pytest

from traveltimepy.async_client import AsyncClient
from traveltimepy.requests.common import (
    Snapping,
    SnappingAcceptRoads,
    SnappingPenalty,
    Property,
    Location,
    Coordinates,
)
from traveltimepy.requests.routes import RoutesDepartureSearch, RoutesArrivalSearch
from traveltimepy.requests.transportation import Driving


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient, locations):
    results = await async_client.routes(
        locations=locations,
        arrival_searches=[],
        departure_searches=[
            RoutesDepartureSearch(
                id="id",
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_location_id="London center",
                departure_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
            )
        ],
    )
    assert len(results) == 1


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient, locations):
    results = await async_client.routes(
        locations=locations,
        departure_searches=[],
        arrival_searches=[
            RoutesArrivalSearch(
                id="id",
                arrival_location_id="London center",
                departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                arrival_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
            )
        ],
    )
    assert len(results) == 1


@pytest.mark.asyncio
async def test_snapping(async_client: AsyncClient):
    locations: List[Location] = [
        Location(id="A", coords=Coordinates(lat=53.806479, lng=-2.615711)),
        Location(id="B", coords=Coordinates(lat=53.810129, lng=-2.601099)),
    ]
    result_with_penalty = await async_client.routes(
        locations=locations,
        arrival_searches=[
            RoutesArrivalSearch(
                id="id",
                arrival_location_id="B",
                departure_location_ids=["A"],
                arrival_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
            )
        ],
        departure_searches=[],
    )
    traveltime_with_penalty = (
        result_with_penalty[0].locations[0].properties[0].travel_time
    )
    result_without_penalty = await async_client.routes(
        locations=locations,
        arrival_searches=[
            RoutesArrivalSearch(
                id="id",
                arrival_location_id="B",
                departure_location_ids=["A"],
                arrival_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
                snapping=Snapping(
                    penalty=SnappingPenalty.DISABLED,
                    accept_roads=SnappingAcceptRoads.ANY_DRIVABLE,
                ),
            )
        ],
        departure_searches=[],
    )
    traveltime_without_penalty = (
        result_without_penalty[0].locations[0].properties[0].travel_time
    )
    assert traveltime_with_penalty is not None
    assert traveltime_without_penalty is not None
    assert traveltime_with_penalty > traveltime_without_penalty
