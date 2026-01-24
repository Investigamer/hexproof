"""
* MTGJSON Schema: Sealed Product
* https://mtgjson.com/data-models/sealed-product/
"""
# Standard Library Imports
from typing import Optional, Union

# Local Imports
from hexproof.mtgjson.schema.__base__ import MTGJsonSchema
from hexproof.mtgjson.schema.identifiers import Identifiers
from hexproof.mtgjson.schema.purchase_urls import PurchaseUrls


class SealedProductCard(MTGJsonSchema):
    """Model describing the 'card' product configuration in SealedProductContents."""
    foil: bool = False
    name: str
    number: str
    set: str
    # Todo: Receiving data from MTGJSON where this field is missing
    uuid: Optional[str] = None


class SealedProductDeck(MTGJsonSchema):
    """Model describing the 'deck' product configuration in SealedProductContents."""
    name: str
    set: str


class SealedProductOther(MTGJsonSchema):
    """Model describing the 'obscure' product configuration in SealedProductContents."""
    name: str


class SealedProductPack(MTGJsonSchema):
    """Model describing the 'pack' product configuration in SealedProductContents."""
    code: str
    set: str


class SealedProductSealed(MTGJsonSchema):
    """Model describing the 'sealed' product configuration in SealedProductContents."""
    count: int
    name: str
    set: str
    # Todo: Receiving data from MTGJSON where this field is missing
    uuid: Optional[str] = None


class SealedProductContentsConfigs(MTGJsonSchema):
    """Utility definition for the 'variable' property on SealedProductContents schema."""
    configs: list['SealedProductContents'] = []


class SealedProductContents(MTGJsonSchema):
    """Model describing the contents properties of a purchasable product in a Set Data Model."""
    card: Optional[list[SealedProductCard]] = []
    deck: Optional[list[SealedProductDeck]] = []
    other: Optional[list[SealedProductOther]] = []
    pack: Optional[list[SealedProductPack]] = []
    sealed: Optional[list[SealedProductSealed]] = []
    variable: Optional[list[SealedProductContentsConfigs]] = []


class SealedProduct(MTGJsonSchema):
    """Model describing the properties for the purchasable product of a Set Data Model."""
    cardCount: Optional[int] = None
    category: Optional[str] = None
    contents: Optional[SealedProductContents] = None
    identifiers: Identifiers
    name: str
    productSize: Optional[int] = None
    purchaseUrls: PurchaseUrls
    releaseDate: Optional[str] = None
    subtype: Union[str | None] = None
    uuid: str
