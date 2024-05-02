"""
* MTG Vectors Enums
"""
# Standard Library Imports
from dataclasses import dataclass

# Third Party Imports
import yarl

"""
* Enums
"""


@dataclass
class URL:
    ROOT = yarl.URL('https://raw.githubusercontent.com/Investigamer/mtg-vectors/main')
    MANIFEST = ROOT / 'manifest.json'
    PACKAGE = ROOT / 'package.zip'
