"""Provides a class for getting unread information."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from datetime import datetime, timezone
from typing import NamedTuple

##############################################################################
# Local imports.
from .prefixes import Prefix, id_is_a
from .session import Session
from .types import OldList, RawData


##############################################################################
class Count(NamedTuple):
    """Unread count information class."""

    id: str
    """The ID of the item that has an unread count."""
    unread: int
    """The unread count."""
    newest_timestamp: datetime
    """The timestamp of the newest item."""
    prefix: str
    """The prefix related to this type of count."""
    raw: RawData | None = None
    """The raw data from the API."""

    @property
    def name(self) -> str:
        """The name of the count."""
        return self.id.removeprefix(self.prefix)

    @classmethod
    def from_json(cls, data: RawData, prefix: str) -> Count:
        """Load the count from JSON data.

        Args:
            data: The data to load the count from.
            prefix: The prefix to associate with this type of count.

        Returns:
            The count information.
        """
        return Count(
            raw=data,
            id=data["id"],
            unread=data["count"],
            newest_timestamp=datetime.fromtimestamp(
                int(data["newestItemTimestampUsec"]) / 1_000_000,
                timezone.utc,
            ),
            prefix=prefix,
        )


##############################################################################
class Counts(OldList[Count]):
    """Holds a collection of [counts][oldas.Count]."""


##############################################################################
class Unread(NamedTuple):
    """Class that loads and holds [unread counts][oldas.Counts]."""

    total: int
    """The total unread count."""
    folders: Counts
    """The unread counts for each folder."""
    feeds: Counts
    """The unread count for each feed."""

    @staticmethod
    def _get_counts(unread: RawData, prefixed_with: Prefix) -> Counts:
        """Get a particular set of unread counts.

        Args:
            unread: The unread data.
            prefix_with: The prefix to look for.

        Returns:
            A list of unread counts of the given prefix.
        """
        return Counts(
            Count.from_json(count, prefixed_with)
            for count in unread["unreadcounts"]
            if id_is_a(count["id"], prefixed_with)
        )

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
