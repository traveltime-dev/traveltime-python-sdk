import asyncio
from collections import deque
from contextlib import asynccontextmanager
from loguru import logger


class Throttler:
    """Simple throttler for asyncio"""

    def __init__(
        self,
        rate_limit: int,
        time_window_seconds: int,
        retry_interval=0.001
    ):
        self.time_window = time_window_seconds
        self.rate_limit = rate_limit
        self.retry_interval = retry_interval

        # Set the event loop to the one passed in, or the default asyncio event loop if none is passed.
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Create a new deque object to store task start times.
        self._task_logs = deque()

    def remove_expired_tasks(self):
        # Get the current time from the event loop
        now = self.loop.time()

        # Remove items (which are start times) that are no longer in the time window
        # Check if the deque containing task start times is not empty.
        while self._task_logs:
            # Calculate the time difference between the current time and the first task start time in the deque,
            # and check whether it's greater than the rate interval length.
            if now - self._task_logs[0] > self.time_window:
                # Remove the first(start time) item from the deque since it's no longer needed.
                self._task_logs.popleft()
            else:
                # If the first item in the deque is still within the time window, break out of the while loop.
                break

    async def __aenter__(self):
        await self.wait_for_availability()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # nothing to do here
        pass

    async def wait_for_availability(self, window_size: int):
        # Start an infinite loop
        while True:
            # get rid of items that don't have to be tracked anymore

            self.remove_expired_tasks()

            # Exit the infinite loop when new task can be processed
            # Check if the task log can accommodate the new task.

            if len(self._task_logs) * window_size + window_size <= self.rate_limit:
                break  # If the rate limit hasn't been reached yet, break out of the infinite loop.

            # calculate the time we have to wait until the task can be processed
            space_available = self.rate_limit - len(self._task_logs) * window_size
            last_task_that_has_to_be_removed = self._task_logs[space_available - 1]
            time_to_wait = max(
                self.retry_interval,
                last_task_that_has_to_be_removed + self.time_window - self.loop.time(),
            )

            logger.debug(
                f"{space_available} available\t"
                f"Waiting {int(time_to_wait)} s..."
            )

            # If the rate limit has been reached, use asyncio.sleep to
            # suspend this coroutine for a short time before trying again.
            await asyncio.sleep(time_to_wait)

        # Push new task's start time
        # If the rate limit hasn't been reached, add the current time as a new start time to the deque.
        time = self.loop.time()
        self._task_logs.append(time)

        logger.debug(
            f"Current Rate: "
            f"{len(self._task_logs) * window_size} / {self.rate_limit} per {self.time_window} s"
        )

    # Define the async context manager enter method
    @asynccontextmanager
    async def use(self, window_size: int):
        """Implementation as context manager method to allow for passing of num_requests parameter"""

        await self.wait_for_availability(window_size)

        yield self  # Return the Throttler object itself as the result of the async context manager enter method.
