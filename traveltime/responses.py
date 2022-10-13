from dataclasses import dataclass

from traveltime import SearchId


@dataclass(frozen=True)
class TimeMapResponse:
    id: SearchId
