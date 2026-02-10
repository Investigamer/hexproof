"""
* MTGJSON Schema: Card Type
* https://mtgjson.com/data-models/card-type/
"""
from hexproof.providers.mtgjson.schema._core import MTGJsonSchema


class CardType(MTGJsonSchema):
    """Model describing the properties of any possible subtypes and supertypes of a CardType Data Model."""
    subTypes: list[str] = []
    superTypes: list[str] = []
