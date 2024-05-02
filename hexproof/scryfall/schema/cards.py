"""
* Parent: Scryfall
* Types: Card Objects
"""
# Standard Library Imports
from typing import Literal, Optional

# Third Party Imports
from omnitils.schema import Schema


"""
* Types
"""

CardLegality: type = Literal['banned', 'legal', 'not_legal', 'restricted']

"""
* Schemas
"""


class CardLegalities(Schema):
    """An object denoting a card's legal, banned, or restricted status for various formats."""
    standard: CardLegality
    future: CardLegality
    historic: CardLegality
    timeless: CardLegality
    gladiator: CardLegality
    pioneer: CardLegality
    explorer: CardLegality
    modern: CardLegality
    legacy: CardLegality
    pauper: CardLegality
    vintage: CardLegality
    penny: CardLegality
    commander: CardLegality
    oathbreaker: CardLegality
    standardbrawl: CardLegality
    brawl: CardLegality
    alchemy: CardLegality
    paupercommander: CardLegality
    duel: CardLegality
    oldschool: CardLegality
    premodern: CardLegality
    predh: CardLegality


class CardRelated(Schema):
    """Represents a symbolic card related to another card."""
    id: str
    object: Literal['related_card']
    component: str
    name: str
    type_line: str
    uri: str


class Card(Schema):
    """Represents a card object on Scryfall.

    Notes:
        See docs: https://scryfall.com/docs/api/cards
    """

    """Core Fields (REQUIRED): Core properties that must be defined."""
    id: str
    lang: str
    object: Literal['card']
    layout: str
    uri: str
    prints_search_uri: str
    rulings_uri: str
    scryfall_uri: str

    """Core Fields (OPTIONAL): Core properties that might not be defined."""
    arena_id: Optional[int]
    mtgo_id: Optional[int]
    mtgo_foil_id: Optional[int]
    multiverse_ids: Optional[list[int]]
    tcgplayer_id: Optional[int]
    tcgplayer_etched_id: Optional[int]
    cardmarket_id: Optional[int]
    oracle_id: Optional[int]

    """Gameplay Fields (REQUIRED): Properties relevant to the game rules that must be defined."""
    cmc: float
    color_identity: list[str]
    keywords: list[str]
    legalities: CardLegalities
    name: str
    reserved: bool
    type_line: str

    """Gameplay Fields (OPTIONAL): Properties relevant to the game rules that might not be defined."""
    # Todo
    all_parts: Optional[list[CardRelated]]

    """Print Fields (REQUIRED): Properties unique to a specific card printing that must be defined."""
    # Todo
    booster: bool

    """Print Fields (OPTIONAL): Properties unique to a specific card printing that might not be defined."""
    # Todo:
    artist: str
