"""
* MTGJSON Schema: Set List
* https://mtgjson.com/data-models/set-list/
"""
# Standard Library Imports
from typing import Optional

from hexproof.mtgjson.schema import DeckSet
# Local Imports
from hexproof.mtgjson.schema.__base__ import MTGJsonSchema
from hexproof.mtgjson.schema.sealed_product import SealedProduct
from hexproof.mtgjson.schema.translations import Translations


class SetList(MTGJsonSchema):
    """Model describing the metadata properties of an individual Set."""
    baseSetSize: int
    block: Optional[str] = None
    cardsphereSetId: Optional[int] = None
    code: str
    codeV3: Optional[str] = None
    decks: Optional[list[DeckSet]] = None
    isForeignOnly: Optional[bool] = None
    isFoilOnly: bool = False
    isNonFoilOnly: Optional[bool] = None
    isOnlineOnly: bool = False
    isPaperOnly: Optional[bool] = None
    isPartialPreview: Optional[bool] = None
    keyruneCode: str
    languages: Optional[list[str]] = None
    mcmId: Optional[int] = None
    mcmIdExtras: Optional[int] = None
    mcmName: Optional[str] = None
    mtgoCode: Optional[str] = None
    name: str
    parentCode: Optional[str] = None
    releaseDate: str
    sealedProduct: Optional[list[SealedProduct]] = None
    tcgplayerGroupId: Optional[int] = None
    totalSetSize: int
    tokenSetCode: Optional[str] = None
    translations: Translations
    type: str
