"""
* Metadata Schemas
"""
# Third Party Imports
from omnitils.schema import Schema

"""
* Schemas
"""


class MetaSchema(Schema):
    """Object schema for Meta resources."""
    resource: str
    version: str
    date: str
    uri: str | None
