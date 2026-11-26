import hashlib
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import (
    Any,
    ClassVar,
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from pydantic import TypeAdapter
from pydantic_core import to_jsonable_python

from traveltimepy.matrix.plan import Direction, Search
from traveltimepy.matrix.result import SearchResult
from traveltimepy.requests.common import (
    ArrivalTimePeriod,
    Coordinates,
    Coords,
    Fares,
    Location,
    Property,
    Snapping,
)
from traveltimepy.requests.time_filter import (
    TimeFilterArrivalSearch,
    TimeFilterDepartureSearch,
    TimeFilterTransportation,
)
from traveltimepy.requests.time_filter_fast import (
    TimeFilterFastArrivalSearches,
    TimeFilterFastManyToOne,
    TimeFilterFastOneToMany,
    TimeFilterFastTransportation,
)
from traveltimepy.requests.time_filter_proto import (
    ProtoCountry,
    RequestType,
    TimeFilterFastProtoTransportation,
)
from traveltimepy.responses.time_filter_fast import Fares as FastFares
from traveltimepy.responses.time_filter_proto import TimeFilterProtoResponse

F = TypeVar("F")


class MatrixBackend(ABC, Generic[F]):
    """Turns planned searches into calls of one endpoint and its responses back into
    matrix values.

    `send` calls the client's endpoint method, so it returns a response for a sync
    client and an awaitable for an async one.
    """

    endpoint: str
    max_searches_per_request: int
    max_points_per_search: int
    max_points_per_request: int
    fares_adapter: ClassVar[TypeAdapter[Any]]

    def __init__(
        self,
        origins: Sequence[Any],
        destinations: Sequence[Any],
        with_distance: bool,
        with_fares: bool,
    ):
        self.origins = origins
        self.destinations = destinations
        self.with_distance = with_distance
        self.with_fares = with_fares

    @property
    def direction(self) -> Optional[Direction]:
        return None

    @abstractmethod
    def _params(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def send(self, client: Any, direction: Direction, searches: List[Search]) -> Any:
        pass

    @abstractmethod
    def parse(
        self, direction: Direction, searches: List[Search], response: Any
    ) -> List[SearchResult[F]]:
        pass

    def fingerprint(self) -> str:
        inputs = {
            "endpoint": self.endpoint,
            "origins": self.origins,
            "destinations": self.destinations,
            "with_distance": self.with_distance,
            "with_fares": self.with_fares,
            "params": self._params(),
        }
        encoded = json.dumps(to_jsonable_python(inputs), sort_keys=True)
        return hashlib.sha256(encoded.encode()).hexdigest()

    def to_record(self, search: Search, result: SearchResult[F]) -> Dict[str, Any]:
        return {
            "search": search.id,
            "travel_times": result.travel_times,
            "distances": result.distances,
            "fares": self.fares_adapter.dump_python(result.fares, mode="json"),
        }

    def from_record(self, record: Dict[str, Any]) -> SearchResult[F]:
        return SearchResult(
            travel_times=record["travel_times"],
            distances=record["distances"],
            fares=self.fares_adapter.validate_python(record["fares"]),
        )

    def _anchor_and_others(
        self, direction: Direction
    ) -> Tuple[Sequence[Any], Sequence[Any]]:
        if direction == Direction.ONE_TO_MANY:
            return self.origins, self.destinations
        return self.destinations, self.origins

    def _empty(self, search: Search) -> SearchResult[F]:
        size = search.end - search.start
        return SearchResult(
            travel_times=[None] * size,
            distances=[None] * size if self.with_distance else None,
            fares=[None] * size if self.with_fares else None,
        )


class _JsonBackend(MatrixBackend[F]):
    max_searches_per_request = 10

    def _properties(self) -> List[Property]:
        properties = [Property.TRAVEL_TIME]
        if self.with_distance:
            properties.append(Property.DISTANCE)
        if self.with_fares:
            properties.append(Property.FARES)
        return properties

    @staticmethod
    def _ids(direction: Direction) -> Tuple[str, str]:
        return ("o", "d") if direction == Direction.ONE_TO_MANY else ("d", "o")

    def _locations(
        self, direction: Direction, searches: List[Search]
    ) -> List[Location]:
        anchors, others = self._anchor_and_others(direction)
        anchor_prefix, other_prefix = self._ids(direction)
        anchor_indices = sorted({search.anchor for search in searches})
        other_indices = sorted(
            {i for search in searches for i in range(search.start, search.end)}
        )
        return [
            Location(id=f"{anchor_prefix}{i}", coords=anchors[i])
            for i in anchor_indices
        ] + [Location(id=f"{other_prefix}{i}", coords=others[i]) for i in other_indices]

    @abstractmethod
    def _values(self, location: Any) -> Tuple[int, Optional[int], Optional[F]]:
        pass

    def parse(
        self, direction: Direction, searches: List[Search], response: Any
    ) -> List[SearchResult[F]]:
        results = {result.search_id: result for result in response.results}
        parsed = []
        for search in searches:
            values = self._empty(search)
            for location in results[search.id].locations:
                index = int(location.id[1:]) - search.start
                travel_time, distance, fares = self._values(location)
                values.travel_times[index] = travel_time
                if values.distances is not None:
                    values.distances[index] = distance
                if values.fares is not None:
                    values.fares[index] = fares
            parsed.append(values)
        return parsed


class TimeFilterBackend(_JsonBackend[Fares]):
    endpoint = "time-filter"
    max_points_per_search = 2000
    max_points_per_request = 20_000
    fares_adapter = TypeAdapter(Optional[List[Optional[Fares]]])

    def __init__(
        self,
        origins: Sequence[Coords],
        destinations: Sequence[Coords],
        with_distance: bool,
        with_fares: bool,
        transportation: TimeFilterTransportation,
        travel_time: int,
        departure_time: Optional[datetime],
        arrival_time: Optional[datetime],
        snapping: Optional[Snapping],
    ):
        if (departure_time is None) == (arrival_time is None):
            raise ValueError("Provide exactly one of departure_time or arrival_time")
        super().__init__(origins, destinations, with_distance, with_fares)
        self.transportation = transportation
        self.travel_time = travel_time
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.snapping = snapping

    @property
    def direction(self) -> Optional[Direction]:
        if self.departure_time is not None:
            return Direction.ONE_TO_MANY
        return Direction.MANY_TO_ONE

    def _params(self) -> Dict[str, Any]:
        return {
            "transportation": self.transportation,
            "travel_time": self.travel_time,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "snapping": self.snapping,
        }

    def send(self, client: Any, direction: Direction, searches: List[Search]) -> Any:
        departures = []
        arrivals = []
        if self.departure_time is not None:
            departures = [
                TimeFilterDepartureSearch(
                    id=search.id,
                    departure_location_id=f"o{search.anchor}",
                    arrival_location_ids=[
                        f"d{i}" for i in range(search.start, search.end)
                    ],
                    departure_time=self.departure_time,
                    travel_time=self.travel_time,
                    transportation=self.transportation,
                    properties=self._properties(),
                    snapping=self.snapping,
                )
                for search in searches
            ]
        if self.arrival_time is not None:
            arrivals = [
                TimeFilterArrivalSearch(
                    id=search.id,
                    arrival_location_id=f"d{search.anchor}",
                    departure_location_ids=[
                        f"o{i}" for i in range(search.start, search.end)
                    ],
                    arrival_time=self.arrival_time,
                    travel_time=self.travel_time,
                    transportation=self.transportation,
                    properties=self._properties(),
                    snapping=self.snapping,
                )
                for search in searches
            ]
        return client.time_filter(
            self._locations(direction, searches), departures, arrivals
        )

    def _values(self, location: Any) -> Tuple[int, Optional[int], Optional[Fares]]:
        properties = location.properties[0]
        return properties.travel_time, properties.distance, properties.fares


class TimeFilterFastBackend(_JsonBackend[FastFares]):
    endpoint = "time-filter/fast"
    max_points_per_search = 100_000
    max_points_per_request = 100_000
    fares_adapter = TypeAdapter(Optional[List[Optional[FastFares]]])

    def __init__(
        self,
        origins: Sequence[Coords],
        destinations: Sequence[Coords],
        with_distance: bool,
        with_fares: bool,
        transportation: TimeFilterFastTransportation,
        travel_time: int,
        arrival_time_period: ArrivalTimePeriod,
        snapping: Optional[Snapping],
    ):
        super().__init__(origins, destinations, with_distance, with_fares)
        self.transportation = transportation
        self.travel_time = travel_time
        self.arrival_time_period = arrival_time_period
        self.snapping = snapping

    def _params(self) -> Dict[str, Any]:
        return {
            "transportation": self.transportation,
            "travel_time": self.travel_time,
            "arrival_time_period": self.arrival_time_period,
            "snapping": self.snapping,
        }

    def send(self, client: Any, direction: Direction, searches: List[Search]) -> Any:
        one_to_many = []
        many_to_one = []
        if direction == Direction.ONE_TO_MANY:
            one_to_many = [
                TimeFilterFastOneToMany(
                    id=search.id,
                    departure_location_id=f"o{search.anchor}",
                    arrival_location_ids=[
                        f"d{i}" for i in range(search.start, search.end)
                    ],
                    transportation=self.transportation,
                    travel_time=self.travel_time,
                    properties=self._properties(),
                    arrival_time_period=self.arrival_time_period,
                    snapping=self.snapping,
                )
                for search in searches
            ]
        else:
            many_to_one = [
                TimeFilterFastManyToOne(
                    id=search.id,
                    arrival_location_id=f"d{search.anchor}",
                    departure_location_ids=[
                        f"o{i}" for i in range(search.start, search.end)
                    ],
                    transportation=self.transportation,
                    travel_time=self.travel_time,
                    properties=self._properties(),
                    arrival_time_period=self.arrival_time_period,
                    snapping=self.snapping,
                )
                for search in searches
            ]
        return client.time_filter_fast(
            self._locations(direction, searches),
            TimeFilterFastArrivalSearches(
                one_to_many=one_to_many, many_to_one=many_to_one
            ),
        )

    def _values(self, location: Any) -> Tuple[int, Optional[int], Optional[FastFares]]:
        properties = location.properties
        return properties.travel_time, properties.distance, properties.fares


class TimeFilterProtoBackend(MatrixBackend[int]):
    endpoint = "time-filter/fast/proto"
    max_searches_per_request = 1
    max_points_per_search = 100_000
    max_points_per_request = 100_000
    fares_adapter = TypeAdapter(Optional[List[Optional[int]]])

    def __init__(
        self,
        origins: Sequence[Coordinates],
        destinations: Sequence[Coordinates],
        with_distance: bool,
        with_fares: bool,
        transportation: TimeFilterFastProtoTransportation,
        travel_time: int,
        country: ProtoCountry,
    ):
        super().__init__(origins, destinations, with_distance, with_fares)
        self.transportation = transportation
        self.travel_time = travel_time
        self.country = country

    def _params(self) -> Dict[str, Any]:
        return {
            "transportation": self.transportation,
            "travel_time": self.travel_time,
            "country": self.country,
        }

    def send(self, client: Any, direction: Direction, searches: List[Search]) -> Any:
        (search,) = searches
        anchors, others = self._anchor_and_others(direction)
        return client.time_filter_fast_proto(
            anchors[search.anchor],
            list(others[search.start : search.end]),
            self.transportation,
            self.travel_time,
            (
                RequestType.ONE_TO_MANY
                if direction == Direction.ONE_TO_MANY
                else RequestType.MANY_TO_ONE
            ),
            self.country,
            self.with_distance,
            self.with_fares,
        )

    def parse(
        self,
        direction: Direction,
        searches: List[Search],
        response: TimeFilterProtoResponse,
    ) -> List[SearchResult[int]]:
        (search,) = searches
        values = self._empty(search)
        for index, travel_time in enumerate(response.travel_times):
            if travel_time < 0:
                continue
            values.travel_times[index] = travel_time
            if values.distances is not None:
                values.distances[index] = response.distances[index]
            if values.fares is not None and response.monthly_fares[index] > 0:
                values.fares[index] = response.monthly_fares[index]
        return [values]
