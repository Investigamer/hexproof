"""
* Parent: Scryfall
* Types: Card Objects
"""
# Standard Library Imports
from typing import Literal

# Third Party Imports
from typing_extensions import NotRequired
from omnitils.schema import DictSchema


CardLegality: type = Literal['banned', 'legal', 'not_legal', 'restricted']


class CardLegalities(DictSchema):
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


class CardRelated(DictSchema):
    """Represents a symbolic card related to another card."""
    id: str
    object: Literal['related_card']
    component: str
    name: str
    type_line: str
    uri: str


class Card(DictSchema):
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
    arena_id: NotRequired[int]
    mtgo_id: NotRequired[int]
    mtgo_foil_id: NotRequired[int]
    multiverse_ids: NotRequired[list[int]]
    tcgplayer_id: NotRequired[int]
    tcgplayer_etched_id: NotRequired[int]
    cardmarket_id: NotRequired[int]
    oracle_id: NotRequired[int]

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
    all_parts: NotRequired[list[CardRelated]]

    """Print Fields (REQUIRED): Properties unique to a specific card printing that must be defined."""
    # Todo
    booster: bool

    """Print Fields (OPTIONAL): Properties unique to a specific card printing that might not be defined."""
    # Todo:
    artist: str
