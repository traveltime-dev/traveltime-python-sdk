import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
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


@dataclass
class MatrixEndpoint(ABC, Generic[F]):
    """Turns planned searches into calls of one endpoint and its responses back into
    matrix values.

    `send` calls the client's endpoint method, so it returns a response for a sync
    client and an awaitable for an async one.
    """

    name: ClassVar[str]
    max_searches_per_request: ClassVar[int]
    max_points_per_search: ClassVar[int]
    max_points_per_request: ClassVar[int]
    fares_adapter: ClassVar[TypeAdapter[Any]]

    origins: Sequence[Any]
    destinations: Sequence[Any]
    with_distance: bool
    with_fares: bool

    @property
    def direction(self) -> Optional[Direction]:
        return None

    @abstractmethod
    def send(self, client: Any, direction: Direction, searches: List[Search]) -> Any:
        pass

    @abstractmethod
    def parse(
        self, direction: Direction, searches: List[Search], response: Any
    ) -> List[SearchResult[F]]:
        pass

    def fingerprint(self) -> str:
        inputs = {"endpoint": self.name, "inputs": to_jsonable_python(self)}
        encoded = json.dumps(inputs, sort_keys=True)
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


@dataclass
class _JsonEndpoint(MatrixEndpoint[F]):
    max_searches_per_request: ClassVar[int] = 10

    def _properties(self) -> List[Property]:
        properties = [Property.TRAVEL_TIME]
        if self.with_distance:
            properties.append(Property.DISTANCE)
        if self.with_fares:
            properties.append(Property.FARES)
        return properties

    @staticmethod
    def _prefixes(direction: Direction) -> Tuple[str, str]:
        return ("o", "d") if direction == Direction.ONE_TO_MANY else ("d", "o")

    def _location_ids(
        self, direction: Direction, search: Search
    ) -> Tuple[str, List[str]]:
        anchor_prefix, other_prefix = self._prefixes(direction)
        others = [f"{other_prefix}{i}" for i in range(search.start, search.end)]
        return f"{anchor_prefix}{search.anchor}", others

    def _locations(
        self, direction: Direction, searches: List[Search]
    ) -> List[Location]:
        anchors, others = self._anchor_and_others(direction)
        anchor_prefix, other_prefix = self._prefixes(direction)
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


@dataclass
class TimeFilterEndpoint(_JsonEndpoint[Fares]):
    name: ClassVar[str] = "time-filter"
    max_points_per_search: ClassVar[int] = 2000
    max_points_per_request: ClassVar[int] = 20_000
    fares_adapter: ClassVar[TypeAdapter[Any]] = TypeAdapter(
        Optional[List[Optional[Fares]]]
    )

    origins: Sequence[Coords]
    destinations: Sequence[Coords]
    transportation: TimeFilterTransportation
    travel_time: int
    departure_time: Optional[datetime]
    arrival_time: Optional[datetime]
    snapping: Optional[Snapping]

    def __post_init__(self) -> None:
        times = [t for t in (self.departure_time, self.arrival_time) if t is not None]
        if len(times) != 1:
            raise ValueError("Provide exactly one of departure_time or arrival_time")
        self._time = times[0]

    @property
    def direction(self) -> Optional[Direction]:
        if self.departure_time is not None:
            return Direction.ONE_TO_MANY
        return Direction.MANY_TO_ONE

    def send(self, client: Any, direction: Direction, searches: List[Search]) -> Any:
        fields: Dict[str, Any] = {
            "travel_time": self.travel_time,
            "transportation": self.transportation,
            "properties": self._properties(),
            "snapping": self.snapping,
        }
        departures = []
        arrivals = []
        for search in searches:
            anchor, others = self._location_ids(direction, search)
            if direction == Direction.ONE_TO_MANY:
                departures.append(
                    TimeFilterDepartureSearch(
                        id=search.id,
                        departure_location_id=anchor,
                        arrival_location_ids=others,
                        departure_time=self._time,
                        **fields,
                    )
                )
            else:
                arrivals.append(
                    TimeFilterArrivalSearch(
                        id=search.id,
                        arrival_location_id=anchor,
                        departure_location_ids=others,
                        arrival_time=self._time,
                        **fields,
                    )
                )
        return client.time_filter(
            self._locations(direction, searches), departures, arrivals
        )

    def _values(self, location: Any) -> Tuple[int, Optional[int], Optional[Fares]]:
        properties = location.properties[0]
        return properties.travel_time, properties.distance, properties.fares


@dataclass
class TimeFilterFastEndpoint(_JsonEndpoint[FastFares]):
    name: ClassVar[str] = "time-filter/fast"
    max_points_per_search: ClassVar[int] = 100_000
    max_points_per_request: ClassVar[int] = 100_000
    fares_adapter: ClassVar[TypeAdapter[Any]] = TypeAdapter(
        Optional[List[Optional[FastFares]]]
    )

    origins: Sequence[Coords]
    destinations: Sequence[Coords]
    transportation: TimeFilterFastTransportation
    travel_time: int
    arrival_time_period: ArrivalTimePeriod
    snapping: Optional[Snapping]

    def send(self, client: Any, direction: Direction, searches: List[Search]) -> Any:
        fields: Dict[str, Any] = {
            "transportation": self.transportation,
            "travel_time": self.travel_time,
            "properties": self._properties(),
            "arrival_time_period": self.arrival_time_period,
            "snapping": self.snapping,
        }
        one_to_many = []
        many_to_one = []
        for search in searches:
            anchor, others = self._location_ids(direction, search)
            if direction == Direction.ONE_TO_MANY:
                one_to_many.append(
                    TimeFilterFastOneToMany(
                        id=search.id,
                        departure_location_id=anchor,
                        arrival_location_ids=others,
                        **fields,
                    )
                )
            else:
                many_to_one.append(
                    TimeFilterFastManyToOne(
                        id=search.id,
                        arrival_location_id=anchor,
                        departure_location_ids=others,
                        **fields,
                    )
                )
        return client.time_filter_fast(
            self._locations(direction, searches),
            TimeFilterFastArrivalSearches(
                one_to_many=one_to_many, many_to_one=many_to_one
            ),
        )

    def _values(self, location: Any) -> Tuple[int, Optional[int], Optional[FastFares]]:
        properties = location.properties
        return properties.travel_time, properties.distance, properties.fares


@dataclass
class TimeFilterProtoEndpoint(MatrixEndpoint[int]):
    name: ClassVar[str] = "time-filter/fast/proto"
    max_searches_per_request: ClassVar[int] = 1
    max_points_per_search: ClassVar[int] = 100_000
    max_points_per_request: ClassVar[int] = 100_000
    fares_adapter: ClassVar[TypeAdapter[Any]] = TypeAdapter(
        Optional[List[Optional[int]]]
    )

    origins: Sequence[Coordinates]
    destinations: Sequence[Coordinates]
    transportation: TimeFilterFastProtoTransportation
    travel_time: int
    country: ProtoCountry

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
