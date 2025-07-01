from datetime import datetime
from typing import List

import pytest

from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import (
    Snapping,
    SnappingAcceptRoads,
    SnappingPenalty,
    Property,
    Location,
    Coordinates,
)
from traveltimepy.requests.routes import RoutesDepartureSearch, RoutesArrivalSearch
from traveltimepy.requests.transportation import Driving, PublicTransport


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient, locations):
    response = await async_client.routes(
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
            ),
            RoutesDepartureSearch(
                id="id 2",
                arrival_location_ids=["Hyde Park", "London center"],
                departure_location_id="ZSL London Zoo",
                departure_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
            ),
        ],
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient, locations):
    response = await async_client.routes(
        locations=locations,
        departure_searches=[],
        arrival_searches=[
            RoutesArrivalSearch(
                id="id",
                arrival_location_id="London center",
                departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[Property.TRAVEL_TIME],
            ),
            RoutesArrivalSearch(
                id="id 2",
                arrival_location_id="ZSL London Zoo",
                departure_location_ids=["Hyde Park", "London center"],
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[Property.TRAVEL_TIME],
            ),
        ],
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_snapping(async_client: AsyncClient):
    locations: List[Location] = [
        Location(id="A", coords=Coordinates(lat=53.806479, lng=-2.615711)),
        Location(id="B", coords=Coordinates(lat=53.810129, lng=-2.601099)),
    ]
    result_with_penalty = await async_client.routes(
        locations=locations,
        departure_searches=[
            RoutesDepartureSearch(
                id="id",
                departure_location_id="B",
                arrival_location_ids=["A"],
                departure_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
            )
        ],
        arrival_searches=[],
    )
    traveltime_with_penalty = (
        result_with_penalty.results[0].locations[0].properties[0].travel_time
    )
    result_without_penalty = await async_client.routes(
        locations=locations,
        departure_searches=[
            RoutesDepartureSearch(
                id="id",
                departure_location_id="B",
                arrival_location_ids=["A"],
                departure_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
                snapping=Snapping(
                    penalty=SnappingPenalty.DISABLED,
                    accept_roads=SnappingAcceptRoads.ANY_DRIVABLE,
                ),
            )
        ],
        arrival_searches=[],
    )
    traveltime_without_penalty = (
        result_without_penalty.results[0].locations[0].properties[0].travel_time
    )
    assert traveltime_with_penalty is not None
    assert traveltime_without_penalty is not None
    assert traveltime_with_penalty > traveltime_without_penalty


def test_departures_sync(client: Client, locations):
    response = client.routes(
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
            ),
            RoutesDepartureSearch(
                id="id 2",
                arrival_location_ids=["Hyde Park", "London center"],
                departure_location_id="ZSL London Zoo",
                departure_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
            ),
        ],
    )
    assert len(response.results) == 2


def test_arrivals_sync(client: Client, locations):
    response = client.routes(
        locations=locations,
        departure_searches=[],
        arrival_searches=[
            RoutesArrivalSearch(
                id="id",
                arrival_location_id="London center",
                departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[Property.TRAVEL_TIME],
            ),
            RoutesArrivalSearch(
                id="id 2",
                arrival_location_id="ZSL London Zoo",
                departure_location_ids=["Hyde Park", "London center"],
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[Property.TRAVEL_TIME],
            ),
        ],
    )
    assert len(response.results) == 2


def test_snapping_sync(client: Client):
    locations: List[Location] = [
        Location(id="A", coords=Coordinates(lat=53.806479, lng=-2.615711)),
        Location(id="B", coords=Coordinates(lat=53.810129, lng=-2.601099)),
    ]
    result_with_penalty = client.routes(
        locations=locations,
        departure_searches=[
            RoutesDepartureSearch(
                id="id",
                departure_location_id="B",
                arrival_location_ids=["A"],
                departure_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
            )
        ],
        arrival_searches=[],
    )
    traveltime_with_penalty = (
        result_with_penalty.results[0].locations[0].properties[0].travel_time
    )
    result_without_penalty = client.routes(
        locations=locations,
        departure_searches=[
            RoutesDepartureSearch(
                id="id",
                departure_location_id="B",
                arrival_location_ids=["A"],
                departure_time=datetime.now(),
                transportation=Driving(),
                properties=[Property.TRAVEL_TIME],
                snapping=Snapping(
                    penalty=SnappingPenalty.DISABLED,
                    accept_roads=SnappingAcceptRoads.ANY_DRIVABLE,
                ),
            )
        ],
        arrival_searches=[],
    )
    traveltime_without_penalty = (
        result_without_penalty.results[0].locations[0].properties[0].travel_time
    )
    assert traveltime_with_penalty is not None
    assert traveltime_without_penalty is not None
    assert traveltime_with_penalty > traveltime_without_penalty
