import pytest

from traveltimepy import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Coordinates, GeohashCentroid, CellProperty
from traveltimepy.requests.geohash_fast import (
    GeoHashFastSearch,
    GeoHashFastArrivalSearches,
    GeoHashFastUnion,
    GeoHashFastIntersection,
)
from traveltimepy.requests.transportation import (
    DrivingFerryFast,
    FastTrafficModel,
    PublicTransportFast,
)


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient):
    response = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient):
    response = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[],
            many_to_one=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
            ],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 2


def test_one_to_many_sync(client: Client):
    response = client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 2


def test_many_to_one_sync(client: Client):
    response = client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[],
            many_to_one=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
            ],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_one_to_many_with_traffic_model(async_client: AsyncClient):
    response = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=DrivingFerryFast(
                        traffic_model=FastTrafficModel.PEAK
                    ),
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 1


@pytest.mark.asyncio
async def test_many_to_one_with_traffic_model(async_client: AsyncClient):
    response = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[],
            many_to_one=[
                GeoHashFastSearch(
                    id="id",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=DrivingFerryFast(
                        traffic_model=FastTrafficModel.OFF_PEAK
                    ),
                    travel_time=900,
                ),
            ],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 1


def test_one_to_many_with_traffic_model_sync(client: Client):
    response = client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=DrivingFerryFast(
                        traffic_model=FastTrafficModel.PEAK
                    ),
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 1


def test_many_to_one_with_traffic_model_sync(client: Client):
    response = client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[],
            many_to_one=[
                GeoHashFastSearch(
                    id="id",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=DrivingFerryFast(
                        traffic_model=FastTrafficModel.OFF_PEAK
                    ),
                    travel_time=900,
                ),
            ],
        ),
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        resolution=6,
    )

    assert len(response.results) == 1


@pytest.mark.asyncio
async def test_union_one_to_many(async_client: AsyncClient):
    response = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        ),
        resolution=6,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        unions=[GeoHashFastUnion(id="union", search_ids=["id", "id 2"])],
    )

    assert len(response.results) == 3


@pytest.mark.asyncio
async def test_intersection_many_to_one(async_client: AsyncClient):
    response = await async_client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            many_to_one=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        ),
        resolution=6,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        intersections=[
            GeoHashFastIntersection(id="intersection", search_ids=["id", "id 2"])
        ],
    )

    assert len(response.results) == 3


def test_union_one_to_many_sync(client: Client):
    response = client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            one_to_many=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
            ],
            many_to_one=[],
        ),
        resolution=6,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        unions=[GeoHashFastUnion(id="union", search_ids=["id", "id 2"])],
    )

    assert len(response.results) == 3


def test_intersection_many_to_one_sync(client: Client):
    response = client.geohash_fast(
        arrival_searches=GeoHashFastArrivalSearches(
            many_to_one=[
                GeoHashFastSearch(
                    id="id",
                    coords=Coordinates(lat=51.507609, lng=-0.128315),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
                GeoHashFastSearch(
                    id="id 2",
                    coords=GeohashCentroid(geohash_centroid="gcpvj3"),
                    transportation=PublicTransportFast(),
                    travel_time=900,
                ),
            ],
            one_to_many=[],
        ),
        resolution=6,
        properties=[CellProperty.MIN, CellProperty.MAX, CellProperty.MEAN],
        intersections=[
            GeoHashFastIntersection(id="intersection", search_ids=["id", "id 2"])
        ],
    )

    assert len(response.results) == 3


def test_remove_water_bodies_drops_cells_over_the_thames_sync(client: Client):
    def cells(remove_water_bodies):
        response = client.geohash_fast(
            arrival_searches=GeoHashFastArrivalSearches(
                one_to_many=[
                    GeoHashFastSearch(
                        id="id",
                        coords=Coordinates(lat=51.5066, lng=-0.1176),
                        transportation=DrivingFerryFast(),
                        travel_time=600,
                        remove_water_bodies=remove_water_bodies,
                    )
                ],
                many_to_one=[],
            ),
            properties=[CellProperty.MEAN],
            resolution=7,
        )
        return {cell.id for cell in response.results[0].cells}

    with_water, without_water = cells(False), cells(True)
    assert without_water < with_water
