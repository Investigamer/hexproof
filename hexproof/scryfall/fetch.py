"""
* Scryfall Request Handling
"""
# Third Party Imports
from pathlib import Path
from typing import Callable, Optional

# Third Party Imports
import requests
import yarl
from omnitils.fetch import request_header_default, download_file
from omnitils.strings import normalize_str
from ratelimit import sleep_and_retry, RateLimitDecorator
from backoff import on_exception, expo
from requests import RequestException

# Local Imports
from hexproof.scryfall.enums import ScryURL
from hexproof.scryfall import schema as ScrySchema

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
* Request Utilities
"""


@request_handler_scryfall
def get_json(url: yarl.URL, header: Optional[dict] = None) -> dict:
    """Retrieves JSON results from a Scryfall API request using the proper rate limits.

    Args:
        url: Scryfall API request URL.
        header: Optional headers to include in the response.

    Returns:
        Dict containing data from the JSON response.
    """
    if header is None:
        header = request_header_default.copy()
    with requests.get(url, headers=header) as r:
        r.raise_for_status()
        return r.json()


def get_paginated_list(
    url: yarl.URL,
    list_object: ScrySchema.ScryfallListSchema = ScrySchema.ListObject,
    header: Optional[dict] = None
) -> ScrySchema.ScryfallList:
    """Processes a Scryfall API request which returns paginated results, appending each page of results to
        the first ListObject gathered.

    Args:
        url: Scryfall API request URL.
        list_object: Scryfall schema to use when processing the ListObject returned.
        header: Optional headers to include in the response.

    Returns:
        A ListObject (CardList, SetList, etc) containing the results of all pages.
    """

    # Grab the first page
    obj = list_object(
        **get_json(
            url=url,
            header=header))

    # Append the next page of results
    if obj.has_more and obj.next_page:
        obj.data.extend(
            get_paginated_list(
                url=yarl.URL(obj.next_page),
                list_object=list_object,
                header=header
            ).data)
    return obj


"""
* Requesting Scryfall Objects
"""


def get_card_named(
    name: str,
    set_code: Optional[str] = None,
    exact: bool = True,
    header: Optional[dict] = None
) -> ScrySchema.Card:
    """Grabs a 'Card' object from Scryfall's `/card/named/{name}` endpoint.

    Args:
        name: The name of the card.
        set_code: Optionally limit the search to one set.
        exact: Whether to use exact name search or fuzzy.
        header: Optional headers to include in the response.

    Returns:
        A Scryfall 'Card' object.
    """

    # Create the base query
    search_method = 'exact' if exact else 'fuzzy'
    query = {search_method: normalize_str(name)}
    if set_code is not None:
        query['set'] = set_code.lower()
    url = ScryURL.API.Cards.Named.with_query(query)

    # Request data
    return ScrySchema.Card(
        **get_json(
            url=url,
            header=header))


def get_set(set_code: str, header: Optional[dict] = None) -> ScrySchema.Set:
    """Grabs a 'Set' object from Scryfall's `/set/{code}` endpoint.

    Args:
        set_code: The set to look for, e.g. MH2
        header: Request header object to pass with request.

    Returns:
        A Scryfall 'Set' object.
    """
    url = ScryURL.API.Sets.All / set_code.lower()

    # Request data
    return ScrySchema.Set(
        **get_json(
            url=url,
            header=header))


"""
* Requesting Listed Scryfall Objects
"""


def get_card_rulings(set_code: str, number: str, header: Optional[dict] = None) -> list[ScrySchema.Ruling]:
    """Grab a 'RulingList' object from Scryfall's `/cards/{code}/{number}/rulings` endpoint and
        return the list of 'Ruling' objects.

    Args:
        set_code: The set code of the card to look for, e.g. MH2
        number: The collector number of the card to look for, as a string.
        header: Request header object to pass with request.

    Returns:
        A list of Scryfall 'Ruling' objects.
    """
    url = ScryURL.API.Cards.Main / set_code.lower() / number / 'rulings'

    # Request data
    return get_paginated_list(
        url=url,
        list_object=ScrySchema.RulingList,
        header=header
    ).data


def get_set_list(header: Optional[dict] = None) -> list[ScrySchema.Set]:
    """Grab a 'SetList' object from Scryfall's `/sets/` endpoint and return the list of 'Set' objects.

    Args:
        header: Request header object to pass with request.

    Returns:
        A list of Scryfall 'Set' objects.
    """
    # Request data
    return ScrySchema.SetList(
        **get_json(
            url=ScryURL.API.Sets.All,
            header=header)
    ).data


"""
* Downloading JSON Assets
"""


@request_handler_scryfall
def cache_set_list(path: Path) -> Path:
    """Stream the current Scryfall 'Sets' resource and save it to a file.

    Args:
        path: Path object where the JSON data will be saved.

    Returns:
        Path where the JSON file was saved.
    """
    download_file(
        url=ScryURL.API.Sets.All,
        path=path)
    return path
