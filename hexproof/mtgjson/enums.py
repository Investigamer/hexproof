"""
* MTGJSON Enums
"""
# Standard Library Imports
from dataclasses import dataclass

# Third Party Imports
import yarl

"""
* Enums
"""


@dataclass
class MTGJsonURL:
    ROOT = yarl.URL('https://mtgjson.com')
    API = ROOT / 'api' / 'v5'
    API_SET_LIST = API / 'SetList.json'
    API_SET_ALL = API / 'AllSetFiles.tar.gz'
    API_META = API / 'Meta.json'
