"""
* MTGJSON Types
"""
# Standard Library Imports
from typing import Literal, Optional

# Third Party Imports
from omnitils.schema import Schema
from pydantic import Field

"""
* Types: Metadata
"""


class Meta(Schema):
    """Model describing the properties of the MTGJSON application meta data."""
    date: str
    version: str


"""
* Types: Translations
"""


# Translations object
class Translations(Schema):
    Ancient_Greek: Optional[str] = Field(None, alias="Ancient Greek")
    Arabic: Optional[str] = Field(None, alias="Arabic")
    Chinese_Simplified: Optional[str] = Field(None, alias="Chinese Simplified")
    Chinese_Traditional: Optional[str] = Field(None, alias="Chinese Traditional")
    French: Optional[str] = Field(None, alias="French")
    German: Optional[str] = Field(None, alias="German")
    Hebrew: Optional[str] = Field(None, alias="Hebrew")
    Italian: Optional[str] = Field(None, alias="Italian")
    Japanese: Optional[str] = Field(None, alias="Japanese")
    Korean: Optional[str] = Field(None, alias="Korean")
    Latin: Optional[str] = Field(None, alias="Latin")
    Phyrexian: Optional[str] = Field(None, alias="Phyrexian")
    Portuguese_Brazil: Optional[str] = Field(None, alias="Portuguese (Brazil)")
    Russian: Optional[str] = Field(None, alias="Russian")
    Sanskrit: Optional[str] = Field(None, alias="Sanskrit")
    Spanish: Optional[str] = Field(None, alias="Spanish")


"""
* Types: Identifiers
"""


class Identifiers(Schema):
    """Model describing the properties of identifiers associated to a card."""
    cardKingdomEtchedId: Optional[str]
    cardKingdomFoilId: Optional[str]
    cardKingdomId: Optional[str]
    cardsphereId: Optional[str]
    mcmId: Optional[str]
    mcmMetaId: Optional[str]
    mtgArenaId: Optional[str]
    mtgjsonFoilVersionId: Optional[str]
    mtgjsonNonFoilVersionId: Optional[str]
    mtgjsonV4Id: Optional[str]
    mtgoFoilId: Optional[str]
    mtgoId: Optional[str]
    multiverseId: Optional[str]
    scryfallId: Optional[str]
    scryfallOracleId: Optional[str]
    scryfallIllustrationId: Optional[str]
    tcgplayerProductId: Optional[str]
    tcgplayerEtchedProductId: Optional[str]


"""
* Types: URLs
"""


class PurchaseUrls(Schema):
    """Model describing the properties of links to purchase a product from a marketplace."""
    cardKingdom: Optional[str]
    cardKingdomEtched: Optional[str]
    cardKingdomFoil: Optional[str]
    cardmarket: Optional[str]
    tcgplayer: Optional[str]
    tcgplayerEtched: Optional[str]


"""
* Types: Sealed Product
"""


class SealedProductCard(Schema):
    """Model describing the 'card' product configuration in SealedProductContents."""
    foil: bool
    name: str
    number: str
    set: str
    uuid: str


class SealedProductDeck(Schema):
    """Model describing the 'deck' product configuration in SealedProductContents."""
    name: str
    set: str


class SealedProductOther(Schema):
    """Model describing the 'obscure' product configuration in SealedProductContents."""
    name: str


class SealedProductPack(Schema):
    """Model describing the 'pack' product configuration in SealedProductContents."""
    code: str
    set: str


class SealedProductSealed(Schema):
    """Model describing the 'sealed' product configuration in SealedProductContents."""
    count: int
    name: str
    set: str
    uuid: str


class SealedProductContents(Schema):
    """Model describing the contents properties of a purchasable product in a Set Data Model."""
    card: Optional[list[SealedProductCard]]
    deck: Optional[list[SealedProductDeck]]
    other: Optional[list[SealedProductOther]]
    pack: Optional[list[SealedProductPack]]
    sealed: Optional[list[SealedProductSealed]]
    variable: Optional[list[dict[Literal['configs']], list['SealedProductContents']]]


class SealedProduct(Schema):
    """Model describing the properties for the purchasable product of a Set Data Model."""
    cardCount: Optional[int]
    category: Optional[str]
    contents: Optional[SealedProductContents]
    identifiers: Identifiers
    name: str
    productSize: Optional[int]
    purchaseUrls: PurchaseUrls
    releaseDate: Optional[str]
    subtype: Optional[str]
    uuid: str


"""
* Types: Cards
"""


class CardSet(Schema):
    pass


class CardToken(Schema):
    pass


"""
* Types: Boosters
"""


class BoosterConfig(Schema):
    pass


"""
* Types: Decks
"""


class DeckSet(Schema):
    pass


"""
* Types: Sets
"""


class SetList(Schema):
    """Model describing the meta data properties of an individual Set."""
    baseSetSize: int
    block: Optional[str]
    code: str
    codeV3: Optional[str]
    isForeignOnly: Optional[bool]
    isFoilOnly: bool
    isNonFoilOnly: Optional[bool]
    isOnlineOnly: bool
    isPaperOnly: Optional[bool]
    isPartialPreview: Optional[bool]
    keyruneCode: str
    mcmId: Optional[int]
    mcmIdExtras: Optional[int]
    mcmName: Optional[str]
    mtgoCode: Optional[str]
    name: str
    parentCode: Optional[str]
    releaseDate: str
    sealedProduct: list[SealedProduct]
    tcgplayerGroupId: Optional[int]
    totalSetSize: int
    translations: Translations
    type: str


class Set(Schema):
    """Model describing the properties of an individual set."""
    baseSetSize: int
    block: Optional[str]
    booster: Optional[dict[str, list[BoosterConfig]]]
    cards: list[CardSet]
    cardsphereSetId: Optional[int]
    code: str
    codeV3: Optional[str]
    decks: list[DeckSet]
    isForeignOnly: Optional[bool]
    isFoilOnly: bool
    isNonFoilOnly: Optional[bool]
    isOnlineOnly: bool
    isPaperOnly: Optional[bool]
    isPartialPreview: Optional[bool]
    keyruneCode: str
    languages: Optional[list[str]]
    mcmId: Optional[int]
    mcmIdExtras: Optional[int]
    mcmName: Optional[str]
    mtgoCode: Optional[str]
    name: str
    parentCode: Optional[str]
    releaseDate: str
    sealedProduct: list[SealedProduct]
    tcgplayerGroupId: Optional[int]
    tokens: list[CardToken]
    tokenSetCode: Optional[str]
    totalSetSize: int
    translations: Translations
    type: str
