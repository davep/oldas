"""Provides constants for the states."""

##############################################################################
# Python imports.
from enum import StrEnum


##############################################################################
class State(StrEnum):
    """TheOldReader state names."""

    READ = "user/-/state/com.google/read"
    """An article that has been read."""
    STARRED = "user/-/state/com.google/starred"
    """An article that has been starred."""
    FRESH = "user/-/state/com.google/fresh"
    """An article that is considered fresh."""


### _states.py ends here
