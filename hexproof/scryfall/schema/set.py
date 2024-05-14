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
    arena_code: Optional[str] = None
    block: Optional[str] = None
    block_code: Optional[str] = None
    card_count: int
    code: str
    digital: bool = False
    foil_only: bool = False
    icon_svg_uri: str
    id: str
    mtgo_code: Optional[str] = None
    name: str
    nonfoil_only: bool = False
    object: Literal['set']
    parent_set_code: Optional[str] = None
    printed_size: Optional[int] = None
    released_at: Optional[str] = None
    scryfall_uri: str
    search_uri: str
    set_type: SetTypes
    tcgplayer_id: Optional[int] = None
    uri: str
