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
from omnitils.fetch import request_header_default, download_file
from omnitils.files.archive import unpack_tar_gz

# Local Imports
from hexproof.mtgjson.enums import MTGJsonURL
from hexproof.mtgjson import schema as MTGJsonTypes

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
* Requesting JSON Assets
"""


@request_handler_mtgjson
def get_data_meta() -> MTGJsonTypes.Meta:
    """Get the current MTGJSON 'Meta' resource."""
    with requests.get(
        url=MTGJsonURL.BulkJSON.Meta,
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        meta_obj = res.json().get('data', {})
        return MTGJsonTypes.Meta(**meta_obj)


@request_handler_mtgjson
def get_data_set(card_set: str) -> MTGJsonTypes.Set:
    """Get a target MTGJSON 'Set' resource.

    Args:
        card_set: The set to look for, e.g. MH2

    Returns:
        MTGJson set dict or empty dict.
    """
    with requests.get(
        url=(MTGJsonURL.API / card_set.upper()).with_suffix('.json'),
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        set_obj = res.json().get('data', {})
        return MTGJsonTypes.Set(**set_obj)


@request_handler_mtgjson
def get_data_set_list() -> list[MTGJsonTypes.SetList]:
    """Get the current MTGJSON 'SetList' resource."""
    with requests.get(
        url=MTGJsonURL.BulkJSON.SetList,
        headers=request_header_default.copy().copy()
    ) as res:
        res.raise_for_status()
        set_list = res.json().get('data', [])
        return [MTGJsonTypes.SetList(**n) for n in set_list]


"""
* Downloading JSON Assets
"""


@request_handler_mtgjson
def get_meta(path: Path) -> Path:
    """Stream a target MTGJSON 'Meta' resource and save it to a file.

    Args:
        path: Path object where the JSON data will be saved.
    """
    download_file(
        url=MTGJsonURL.BulkJSON.Meta,
        path=path)
    return path


@request_handler_mtgjson
def get_set(card_set: str, path: Path) -> Path:
    """Stream a target MTGJSON 'Set' resource and save it to a file.

    Args:
        card_set: The set to look for, ex: MH2
        path: Path object where the JSON data will be saved.
    """
    download_file(
        url=(MTGJsonURL.Sets / card_set.upper()).with_suffix('.json'),
        path=path)
    return path


@request_handler_mtgjson
def get_set_list(path: Path) -> Path:
    """Stream the current MTGJSON 'SetList' resource and save it to a file.

    Args:
        path: Path object where the JSON data will be saved.
    """
    download_file(
        url=MTGJsonURL.BulkJSON.SetList,
        path=path)
    return path


@request_handler_mtgjson
def get_sets_all(path: Path) -> Path:
    """Stream the current MTGJSON 'AllSetFiles' archive, save it, and extract it.

    Args:
        path: Directory to unpack the 'AllSetFiles' MTGJSON archive.

    Returns:
        Path to the unpacked 'AllSetFiles' MTGJSON directory.
    """
    archive = path / 'AllSetFiles.tar.gz'
    download_file(
        url=MTGJsonURL.BulkZip.AllSetFiles,
        path=archive)

    # Unpack the contents
    unpack_tar_gz(archive)
    return Path(path / 'AllSetFiles')
