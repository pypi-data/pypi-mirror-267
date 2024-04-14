import re as regex
from collections.abc import Callable, Iterable, Mapping
from functools import reduce

import requests
import tcrutils as tcr

from .zms_consts import API_URL
from .zms_rate import GLOBAL_DEFAULT_RATE_LIMITER, RateLimiter
from .zms_types import Profile, ProfileInfo, ProfileInfoError


def _get_single_profiles(id: int | str, rl: RateLimiter, announcer: Callable) -> list[Profile]:
  url = API_URL / 'profiles' / id

  rl.sleep_until_over()

  response = requests.get(url).json()

  if announcer is not None:
    for profile in response:
      announcer(id, profile)

  return response


def _get_single_profile(id: int | str, rl: RateLimiter, announcer: Callable) -> ProfileInfo | ProfileInfoError:
  url = API_URL / 'profile' / id

  rl.sleep_until_over()

  response = requests.get(url).json()

  if announcer is not None:
    announcer(id, response)

  return response


def get_profiles(
  *ids: int | str,
  rate_limiter=GLOBAL_DEFAULT_RATE_LIMITER,
  announcer: Callable[[Profile], None] | None = None,
) -> list[Profile]:
  if not ids:
    return []

  if not all(tcr.discord.is_snowflake(x, allow_string=True) for x in ids):
    raise ValueError('All ids must be discord Snowflakes. (int-like strings allowed)')

  ids = [int(x) for x in ids]
  ids = list(set(ids))  # Remove duplicates

  requested = [_get_single_profiles(x, rl=rate_limiter, announcer=announcer) for x in ids]

  return reduce(lambda x, y: x + y, requested)


def get_profile_infos(
  *profiles: Profile,
  rate_limiter=GLOBAL_DEFAULT_RATE_LIMITER,
  announcer: Callable[[ProfileInfo | ProfileInfoError], None] | None = None,
  drop_errored_profiles: bool = False,
) -> list[ProfileInfo | ProfileInfoError]:
  if not profiles:
    return []

  if not all(isinstance(x, dict) for x in profiles) or not all('id' in x for x in profiles):
    raise ValueError("All must be valid profile dictionaries (or at least dictionaries containing the key 'id')")

  r = [profile['id'] for profile in profiles]

  r = [_get_single_profile(x, rl=rate_limiter, announcer=announcer) for x in r]

  if drop_errored_profiles:
    r = [x for x in r if 'error' not in x]

  return r
