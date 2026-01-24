"""
* MTGJSON Schema: Booster
* https://mtgjson.com/data-models/booster/
"""
# Standard Library Imports
from typing import Optional

from pydantic import Field

# Local Imports
from hexproof.mtgjson.schema.__base__ import MTGJsonSchema

"""
* Schemas
"""


class BoosterPack(MTGJsonSchema):
    """Model describing the properties of how a Set's booster data may be configured."""
    contents: dict[str, Optional[int]]
    weight: int


class BoosterSheet(MTGJsonSchema):
    """Model describing the properties of how a sheet of printed cards can be configured."""
    allowDuplicates: Optional[bool] = None
    balanceColors: Optional[bool] = None
    cards: dict[str, int]
    foil: bool
    fixed: Optional[bool] = None
    totalWeight: int


class BoosterConfig(MTGJsonSchema):
    """Model describing the properties of how a Booster Pack can be configured."""
    boosters: list[BoosterPack] = Field(default_factory=list)
    boostersTotalWeight: int
    # Todo: Not documented on MTGJSON docs
    languages: Optional[list[str]] = None
    name: Optional[str] = None
    sheets: dict[str, BoosterSheet] = Field(default_factory=dict)
    sourceSetCodes: list[str] = Field(default_factory=list)


"""
* Types
"""

Booster = dict[str, BoosterConfig]
"""
* A Booster is a data structure with containing property values 
of Booster configurations, and is not a Data Model itself.
"""
