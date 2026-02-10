"""
* MTGJSON Schema: Deck List
* https://mtgjson.com/data-models/deck-list/
"""
from typing import Union

from hexproof.providers.mtgjson.schema._core import MTGJsonSchema


class DeckList(MTGJsonSchema):
    """Model describing the meta data properties of an individual Deck."""
    code: str
    fileName: str
    name: str
    releaseDate: Union[str, None]
    type: str
