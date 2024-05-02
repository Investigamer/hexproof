"""
* Scryfall Data Types
"""
# Standard Library Imports
from typing import Literal, Union, Optional

# Third Party Imports
from omnitils.schema import Schema

"""
* Types
"""

SetTypes = Union[
    Literal['core'],
    Literal['expansion'],
    Literal['masters'],
    Literal['alchemy'],
    Literal['masterpiece'],
    Literal['arsenal'],
    Literal['from_the_vault'],
    Literal['spellbook'],
    Literal['premium_deck'],
    Literal['duel_deck'],
    Literal['draft_innovation'],
    Literal['treasure_chest'],
    Literal['commander'],
    Literal['planechase'],
    Literal['archenemy'],
    Literal['vanguard'],
    Literal['funny'],
    Literal['starter'],
    Literal['box'],
    Literal['promo'],
    Literal['token'],
    Literal['memorabilia'],
    Literal['minigame']
]

"""
* Schemas
"""


class Set(Schema):
    """Scryfall 'Set' object representing a group of related Magic cards."""
    arena_code: Optional[str]
    block: Optional[str]
    block_code: Optional[str]
    card_count: int
    code: str
    digital: bool
    foil_only: bool
    icon_svg_uri: str
    id: str
    mtgo_code: Optional[str]
    name: str
    nonfoil_only: bool
    object: Literal['set']
    parent_set_code: Optional[str]
    printed_size: Optional[int]
    released_at: Optional[str]
    scryfall_uri: str
    search_uri: str
    set_type: SetTypes
    tcgplayer_id: Optional[int]
    uri: str
