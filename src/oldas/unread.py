"""Provides a class for getting unread information."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import Any, NamedTuple

##############################################################################
# Local imports.
from ._prefixes import Prefix
from .session import Session


##############################################################################
class Count(NamedTuple):
    """Unread count information class."""

    id: str
    """The ID of the item that has an unread count."""
    unread: int
    """The unread count."""
    newest_timestamp: int
    """The timestamp of the newest item."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Count:
        """Load the count from JSON data.

        Args:
            data: The data to load the count from.

        Returns:
            The count information.
        """
        return Count(
            id=data["id"],
            unread=data["count"],
            newest_timestamp=data["newestItemTimestampUsec"],
        )


##############################################################################
class Unread(NamedTuple):
    """Class that loads and holds unread counts."""

    total: int
    """The total unread count."""
    folders: list[Count]
    """The unread counts for each folder."""
    feeds: list[Count]
    """The unread count for each feed."""

    @staticmethod
    def _get_counts(unread: dict[str, Any], prefixed_with: Prefix) -> list[Count]:
        return [
            Count.from_json(count)
            for count in unread["unreadcounts"]
            if count["id"].startswith(prefixed_with)
        ]

    @classmethod
    async def load(cls, session: Session) -> Unread:
        """Load the unread counts.

        Args:
            session: The API session object.

        Returns:
            The unread counts.
        """
        unread = await session.get("unread-count")
        return cls(
            total=unread["max"],
            folders=cls._get_counts(unread, Prefix.FOLDER),
            feeds=cls._get_counts(unread, Prefix.FEED),
        )


### unread.py ends here
