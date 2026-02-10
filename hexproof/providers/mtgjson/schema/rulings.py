"""
* MTGJSON Schema: Rulings
* https://mtgjson.com/data-models/rulings/
"""
from hexproof.providers.mtgjson.schema._core import MTGJsonSchema


class Rulings(MTGJsonSchema):
    """Model describing the properties of rulings for a card."""
    date: str
    text: str
