"""
* Scryfall Request Handling
"""
# Third Party Imports
from typing import Callable, Optional

# Third Party Imports
import requests
from omnitils.fetch import request_header_default
from ratelimit import sleep_and_retry, RateLimitDecorator
from backoff import on_exception, expo
from requests import RequestException

# Local Imports
from hexproof.scryfall.enums import ScryURL
from hexproof.scryfall.schema.set import Set

# Rate limiter to safely limit MTGJSON requests
scryfall_rate_limit = RateLimitDecorator(calls=20, period=1)


"""
* Handlers
"""


def request_handler_scryfall(func) -> Callable:
    """Wrapper for a Scryfall request function to handle retries and rate limits.

    Notes:
        Scryfall recommends a 5-10 millisecond delay between requests.
        We target the floor of this recommendation: 20 requests/second.
        Might consider dropping this to 10 requests/second in the future.
        https://scryfall.com/docs/api

    Args:
        func: Scryfall request function to wrap.

    Returns:
        The wrapped function.
    """
    @sleep_and_retry
    @scryfall_rate_limit
    @on_exception(expo, RequestException, max_tries=2, max_time=1)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return decorator


"""
* Request Funcs
"""


@request_handler_scryfall
def get_set(set_code: str, header: Optional[dict] = None) -> Set:
    """Grabs a 'Set' object from Scryfall's `/set/{code}` endpoint.

    Args:
        set_code: The set to look for, e.g. MH2
        header: Request header object to pass with request.

    Returns:
        A Scryfall 'Set' object.
    """
    url = ScryURL.API_SETS / set_code.lower()
    if header is None:
        header = request_header_default.copy()
    with requests.get(url, headers=header) as r:
        r.raise_for_status()
        return r.json()


@request_handler_scryfall
def get_set_list(header: Optional[dict] = None) -> list[Set]:
    """Grab a list of all Scryfall 'Set' objects from their `/sets/` endpoint.

    Args:
        header: Request header object to pass with request.

    Returns:
        A list of every Scryfall 'Set' object.
    """
    if header is None:
        header = request_header_default.copy()
    with requests.get(url=ScryURL.API_SETS, headers=header) as r:
        r.raise_for_status()
        return r.json().get('data', [])
