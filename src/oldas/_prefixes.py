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


### _prefixes.py ends here
