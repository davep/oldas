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
    ARTICLE = "tag:google.com,2005:reader/item/"
    """An article."""


##############################################################################
def id_is_a(item_id: str, prefix: Prefix) -> bool:
    """Does the ID look like it's of a particular type?

    Args:
        item_id: The ID to check.
        prefix: The prefix to test against.

    Returns:
        [`True`][True] if the `item_id` has the provided `prefix`,
        [`False`][False] if not.
    """
    return item_id.startswith(prefix)


##############################################################################
def id_is_a_folder(item_id: str) -> bool:
    """Does the ID look like it's a folder?

    Args:
        item_id: The ID to check.

    Returns:
        [`True`][True] if the ID looks like a folder, [`False`][False] if not.
    """
    return id_is_a(item_id, Prefix.FOLDER)


##############################################################################
def id_is_a_feed(item_id: str) -> bool:
    """Does the ID look like it's a feed?

    Args:
        item_id: The ID to check.

    Returns:
        [`True`][True] if the ID looks like a feed, [`False`][False] if not.
    """
    return id_is_a(item_id, Prefix.FEED)


##############################################################################
def id_is_an_article(item_id: str) -> bool:
    """Does the ID look like it's an article?

    Args:
        item_id: The ID to check.

    Returns:
        [`True`][True] if the ID looks like an article, [`False`][False] if not.
    """
    return id_is_a(item_id, Prefix.ARTICLE)


### prefixes.py ends here
