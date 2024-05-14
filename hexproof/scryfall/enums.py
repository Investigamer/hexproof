"""
* Scryfall Enums
"""
# Standard Library Imports
from dataclasses import dataclass
from omnitils.enums import StrConstant

# Third Party Imports
import yarl

"""
* URL Enums
"""


@dataclass
class ScryURL:
    ROOT = yarl.URL('https://scryfall.com')
    API = yarl.URL('https://api.scryfall.com')
    ROOT_SETS = ROOT / 'sets'
    API_BULK = API / 'bulk-data'
    API_SETS = API / 'sets'
    API_CARDS = API / 'cards'
    API_CARDS_SEARCH = API / 'cards' / 'search'


"""
* Str Enums
"""


class SetType(StrConstant):
    """Set 'types' as defined by Scryfall.

    Notes:
        https://scryfall.com/docs/api/sets
    """
    Core = 'core'
    Expansion = 'expansion'
    Masters = 'masters'
    Alchemy = 'alchemy'
    Masterpiece = 'masterpiece'
    Arsenal = 'arsenal'
    FromTheVault = 'from_the_vault'
    Spellbook = 'spellbook'
    PremiumDeck = 'premium_deck'
    DuelDeck = 'duel_deck'
    DraftInnovation = 'draft_innovation'
    TreasureChest = 'treasure_chest'
    Commander = 'commander'
    Planechase = 'planechase'
    Archenemy = 'archenemy'
    Vanguard = 'vanguard'
    Funny = 'funny'
    Starter = 'starter'
    Box = 'box'
    Promo = 'promo'
    Token = 'token'
    Memorabilia = 'memorabilia'
    Minigame = 'minigame'
