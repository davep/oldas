"""Provides a class for getting article data."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Iterable, Literal, NamedTuple

##############################################################################
# Local imports.
from ._prefixes import id_is_a_folder
from ._states import State
from ._types import OldList, RawData
from .folders import Folder
from .session import Session
from .subscriptions import Subscription

##############################################################################
Direction = Literal["ltr", "rtl"]
"""Possible values for the summary direction."""


##############################################################################
class Summary(NamedTuple):
    """The summary details for an article."""

    direction: Direction
    """The direction for the text in the summary."""
    content: str
    """The content of the summary."""
    raw: RawData | None = None
    """The raw data from the API."""

    @classmethod
    def from_json(cls, data: RawData) -> Summary:
        """Load the summary from JSON data.

        Args:
            data: The data to load the summary from.

        Returns:
            The summary.
        """
        return cls(
            raw=data,
            direction=data["direction"],
            content=data["content"],
        )


##############################################################################
class Origin(NamedTuple):
    """The origin details for an article."""

    stream_id: str | None
    """The stream ID for the article's origin."""
    title: str
    """The title of the origin of the article."""
    html_url: str
    """The URL of the HTML of the origin of the article."""
    raw: RawData | None = None
    """The raw data from the API."""

    @classmethod
    def from_json(cls, data: RawData) -> Origin:
        """Load the origin from JSON data.

        Args:
            data: The data to load the origin from.

        Returns:
            The summary.
        """
        return cls(
            raw=data,
            stream_id=data.get("streamId"),
            title=data["title"],
            html_url=data["htmlUrl"],
        )


##############################################################################
class Article(NamedTuple):
    """Holds details about an article."""

    id: str
    """The ID of the article."""
    title: str
    """The title of the article."""
    published: datetime
    """The time when the article was published."""
    updated: datetime
    """The time when the article was updated."""
    author: str
    """The author of the article."""
    summary: Summary
    """The summary of the article."""
    categories: list[State | str]
    """The list of categories associated with this article."""
    origin: Origin
    """The origin of the article."""
    raw: RawData | None = None
    """The raw data from the API."""

    @property
    def is_read(self) -> bool:
        """Has this article been read?"""
        return State.READ in self.categories

    @property
    def is_unread(self) -> bool:
        """Is the article still unread?"""
        return not self.is_read

    @property
    def is_fresh(self) -> bool:
        """Is the article considered fresh?"""
        return State.FRESH in self.categories

    @property
    def is_stale(self) -> bool:
        """Is the article considered stale?"""
        return not self.is_fresh

    @property
    def is_updated(self) -> bool:
        """Does the article look like it's been updated?"""
        return self.published != self.updated

    async def mark_read(self, session: Session) -> bool:
        """Mark the article as read.

        Args:
            session: The API session object.

        Returns:
            The boolean response from the API.
        """
        return await session.add_tag(self.id, State.READ)

    async def mark_unread(self, session: Session) -> bool:
        """Mark the article as unread.

        Args:
            session: The API session object.

        Returns:
            The boolean response from the API.
        """
        return await session.remove_tag(self.id, State.READ)

    @staticmethod
    def clean_categories(categories: Iterable[str]) -> list[State | str]:
        """Clean up a collection of categories.

        Args:
            categories: The categories to clean up.

        Returns:
            The cleaned categories.
        """
        return [
            category if id_is_a_folder(category) else State(category)
            for category in categories
        ]

    @classmethod
    def from_json(cls, data: RawData) -> Article:
        """Load the article from JSON data.

        Args:
            data: The data to load the article from.

        Returns:
            The article.
        """
        return cls(
            raw=data,
            id=data["id"],
            title=data["title"],
            published=datetime.fromtimestamp(data["published"], timezone.utc),
            updated=datetime.fromtimestamp(data["updated"], timezone.utc),
            author=data["author"],
            summary=Summary.from_json(data["summary"]),
            categories=cls.clean_categories(data["categories"]),
            origin=Origin.from_json(data["origin"]),
        )


##############################################################################
class Articles(OldList[Article]):
    """Loads and holds a full list of articles."""

    @classmethod
    async def stream(
        cls, session: Session, stream: str | Subscription | Folder = "", **filters: Any
    ) -> AsyncIterator[Article]:
        """Load articles from a given stream.

        Args:
            session: The API session object.
            stream: The stream identifier to load from.

        Yields:
            The articles.
        """
        if isinstance(stream, (Folder, Subscription)):
            stream = stream.id
        continuation: str | None = ""
        while True:
            result = await session.get(
                "/stream/contents", s=stream, c=continuation, **filters
            )
            for article in (
                Article.from_json(article) for article in result.get("items", [])
            ):
                yield article
            if not (continuation := result.get("continuation")):
                break

    @classmethod
    async def stream_new_since(
        cls,
        session: Session,
        since: datetime,
        stream: str | Subscription | Folder = "",
        **filters: Any,
    ) -> AsyncIterator[Article]:
        """Stream all articles newer than a given time.

        Args:
            session: The API session object.
            since: Time from which to load articles.
            stream: The stream identifier to stream from.

        Yields:
            Articles.
        """
        async for article in cls.stream(
            session,
            stream,
            ot=int(since.timestamp()),  # codespell:ignore ot,
            # The continuation of "newer than" filtered items seems to not
            # work unless we order the result; so let's go oldest first...
            r="o",
            **filters,
        ):
            yield article


### articles.py ends here
