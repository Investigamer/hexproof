"""
* MTGJSON - Schemas: Base Schemas
"""
from omnitils.schema import Schema
from pydantic import ConfigDict


class MTGJsonSchema(Schema):
    """Base Schema class for MTGJson data models."""
    model_config = ConfigDict(extra="allow")
