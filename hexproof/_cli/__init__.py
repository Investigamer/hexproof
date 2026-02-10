"""
* CLI Application
* Primarily used for testing and development.
"""
from typer import Typer

from hexproof._cli.test import TestCLI

# Export CLI Application
HexproofCLI = Typer()
HexproofCLI.add_typer(TestCLI, name="test")
__all__ = ['HexproofCLI']
