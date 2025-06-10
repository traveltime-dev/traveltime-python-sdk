import os
from typing import List

import pytest

from traveltimepy import Location, Coordinates
from traveltimepy.async_client import AsyncClient


@pytest.fixture
def async_client() -> AsyncClient:
    return AsyncClient(os.environ["APP_ID"], os.environ["API_KEY"])


@pytest.fixture
def locations() -> List[Location]:
    return [
        Location(id="London center", coords=Coordinates(lat=51.508930, lng=-0.131387)),
        Location(id="Hyde Park", coords=Coordinates(lat=51.508824, lng=-0.167093)),
        Location(id="ZSL London Zoo", coords=Coordinates(lat=51.536067, lng=-0.153596)),
    ]
