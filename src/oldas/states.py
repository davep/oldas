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
    KEPT_UNREAD = "user/-/state/com.google/kept-unread"
    """An article was marked by the user to be kept unread."""
    READING_LIST = "user/-/state/com.google/reading-list"
    """The article is part of the user's reading list."""
    BROADCAST = "user/-/state/com.google/broadcast"
    """The article has been shared."""
    LIKE = "user/-/state/com.google/like"
    """The article has been liked."""


### states.py ends here
