"""
* Scryfall Schema: Error
* https://scryfall.com/docs/api/errors
"""
from typing import Literal, Optional

from hexproof.providers.scryfall.schema._core import ScryfallSchema


class Error(ScryfallSchema):
    """An object representing an error returned from the Scryfall API."""
    object: Literal['error'] = 'error'
    status: int
    code: str
    details: str
    type: Optional[str] = None
    warnings: Optional[list[str]] = None
