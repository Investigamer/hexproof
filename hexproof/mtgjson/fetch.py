"""
* MTGJSON Request Handling
"""
# Standard Library Imports
from typing import Callable
from pathlib import Path

# Third Party Imports
import requests
from ratelimit import sleep_and_retry, RateLimitDecorator
from backoff import on_exception, expo
from omnitils.fetch import request_header_default
from omnitils.files.archive import unpack_tar_gz

# Local Imports
from hexproof.mtgjson.enums import MTGJsonURL
from hexproof.mtgjson.schema import types as MTGJsonTypes

# Rate limiter to safely limit MTGJSON requests
mtgjson_rate_limit = RateLimitDecorator(calls=20, period=1)
mtgjson_gql_rate_limit = RateLimitDecorator(calls=20, period=1)


"""
* Handlers
"""


def request_handler_mtgjson(func) -> Callable:
    """Wrapper for MTGJSON request functions to handle retries and rate limits.

    Notes:
        There are no known rate limits for requesting JSON file resources.
        We include a 20-per-second rate limit just to be nice.
    """
    @sleep_and_retry
    @mtgjson_rate_limit
    @on_exception(expo, requests.exceptions.RequestException, max_tries=2, max_time=1)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return decorator


def request_handler_mtgjson_gql(func) -> Callable:
    """Wrapper for MTGJSON GraphQL request functions to handle retries and rate limits.

    Notes:
        MTGJSON GraphQL requests are capped at 500 per-hour per-token at the moment.
        https://mtgjson.com/mtggraphql/#rate-limits
    """
    @sleep_and_retry
    @mtgjson_gql_rate_limit
    @on_exception(expo, requests.exceptions.RequestException, max_tries=2, max_time=1)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return decorator


"""
* Request Funcs
"""


@request_handler_mtgjson
def get_meta() -> MTGJsonTypes.Meta:
    """MTG.Meta: Get the current metadata resource for MTGJSON."""
    with requests.get(
        url=MTGJsonURL.API_META,
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        return res.json().get('data', {})


@request_handler_mtgjson
def get_set(card_set: str) -> MTGJsonTypes.Set:
    """Grab available set data from MTG Json.

    Args:
        card_set: The set to look for, ex: MH2

    Returns:
        MTGJson set dict or empty dict.
    """
    with requests.get(
        url=(MTGJsonURL.API / card_set.upper()).with_suffix('.json'),
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        return res.json().get('data', {})


@request_handler_mtgjson
def get_set_list() -> list[MTGJsonTypes.SetList]:
    """Grab the current 'SetList' MTGJSON file."""
    with requests.get(
        url=MTGJsonURL.API_SET_LIST,
        headers=request_header_default.copy().copy()
    ) as res:
        res.raise_for_status()
        return res.json().get('data', [])


@request_handler_mtgjson
def get_sets_all(path: Path) -> Path:
    """Download the current JSON file archive from the 'AllSetFiles' MTGJSON endpoint.

    Args:
        path: Directory to unpack the 'AllSetFiles' MTGJSON archive.

    Returns:
        Path to the unpacked 'AllSetFiles' MTGJSON directory.
    """
    path = path / 'AllSetFiles.tar.gz'
    res = requests.get(
        url=MTGJsonURL.API_SET_ALL,
        headers=request_header_default.copy().copy())
    with open(path, 'wb') as f:
        f.write(res.content)

    # Unpack the contents
    unpack_tar_gz(path)
    return Path(path.parent) / 'AllSetFiles'
