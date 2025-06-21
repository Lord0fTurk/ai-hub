# src/utils/rate_limiter.py
import asyncio
import time


class RateLimiter:
    """
    Async token bucket rate limiter to restrict number of calls per time period.

    Usage:
        limiter = RateLimiter(max_calls=5, period=1.0)  # 5 calls per 1 second

        async def some_api_call():
            await limiter.acquire()
            # perform API request here
    """

    def __init__(self, max_calls: int, period: float) -> None:
        self.max_calls = max_calls
        self.period = period
        self._tokens = max_calls
        self._last_check = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_check
            # Refill tokens based on elapsed time
            refill_tokens = elapsed * (self.max_calls / self.period)
            self._tokens = min(self.max_calls, self._tokens + refill_tokens)
            self._last_check = now

            if self._tokens >= 1:
                self._tokens -= 1
                return

            # Calculate wait time for next token
            wait_time = (1 - self._tokens) * (self.period / self.max_calls)

        await asyncio.sleep(wait_time)
        # Try again after sleep
        await self.acquire()
