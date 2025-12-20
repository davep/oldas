"""Provides constants for the prefixes used in various IDs in TheOldReader."""

##############################################################################
# Python imports.
from enum import StrEnum


##############################################################################
class Prefix(StrEnum):
    """TheOldReader ID prefixes."""

    FOLDER = "user/-/label/"
    """A folder."""
    FEED = "feed/"
    """A feed."""


##############################################################################
def id_is_a(item_id: str, prefix: Prefix) -> bool:
    """Does the ID look like it's of a particular type?

    Args:
        item_id: The ID to check.
        prefix: The prefix to test against.
    """
    return item_id.startswith(prefix)


### _prefixes.py ends here
