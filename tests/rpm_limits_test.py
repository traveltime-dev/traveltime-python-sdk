import asyncio
import time

import pytest

from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client


@pytest.mark.asyncio
async def test_async_client_10_requests_throttled(async_client_low_rpm: AsyncClient):
    start_time = time.time()

    tasks = []
    for i in range(10):
        task = async_client_low_rpm.geocoding(query=f"Parliament square {i}", limit=1)
        tasks.append(task)

    await asyncio.gather(*tasks)

    elapsed_time = time.time() - start_time

    assert 60 <= elapsed_time < 65  # At least 1 minute due to rate limiting


def test_sync_client_10_requests_throttled(client_low_rpm: Client):
    start_time = time.time()

    for i in range(10):
        client_low_rpm.geocoding(query=f"Parliament square {i}", limit=1)

    elapsed_time = time.time() - start_time

    assert 60 <= elapsed_time < 65  # At least 1 minute due to rate limiting
