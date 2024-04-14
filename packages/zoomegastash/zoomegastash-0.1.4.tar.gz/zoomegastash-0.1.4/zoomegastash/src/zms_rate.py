import time

ONE_TENTH_OF_CURRENT_RATE_LIMIT_ON_THIS_RATE_LIMITER = object()


class RateLimiter:
  """Rate limiter. Sleep for the duration of or check if the rate limit is over."""

  rate_limit_seconds: int
  """Rate limit in seconds. You may change this value on an initialised rate limiter to change its rate limit."""

  def __init__(self, rate_limit_seconds: int):
    self.rate_limit_seconds = rate_limit_seconds
    self._last_request_unix = 0

  def rate_limited(self):
    """Return False if ready for another request. True otherwise.

    If you get True ("keep waiting") you should periodically call this function again to see if the time for your limit passed.
    You may do other work while waiting.

    Example:
    ```py
    do_request()
    while rate_limiter.rate_limitted():
      do_work()
    do_request()
    ```
    """
    if time.time() - self._last_request_unix < self.rate_limit_seconds:
      return True
    self._last_request_unix = time.time()
    return False

  def sleep_until_over(self, check_every_seconds: int = ONE_TENTH_OF_CURRENT_RATE_LIMIT_ON_THIS_RATE_LIMITER):
    """Sleep until rate limit is passed. You may not do other work while this is ongoing, if you wish to do so use :meth:`rate_limited`."""
    if check_every_seconds is ONE_TENTH_OF_CURRENT_RATE_LIMIT_ON_THIS_RATE_LIMITER:
      check_every_seconds = self.rate_limit_seconds / 10

    while self.rate_limited():
      time.sleep(check_every_seconds)


GLOBAL_DEFAULT_RATE_LIMITER = RateLimiter(1)
