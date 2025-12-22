"""Provides a class for getting article data."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from datetime import datetime
from typing import Any, Literal, NamedTuple

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

    raw: RawData
    """The raw data from the API."""
    direction: Direction
    """The direction for the text in the summary."""
    content: str
    """The content of the summary."""

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

    raw: RawData
    """The raw data from the API."""
    stream_id: str | None
    """The stream ID for the article's origin."""
    title: str
    """The title of the origin of the article."""
    html_url: str
    """The URL of the HTML of the origin of the article."""

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

    raw: RawData
    """The raw data from the API."""
    id: str
    """The ID of the article."""
    title: str
    """The title of the article."""
    published: datetime
    """The time when the article was published."""
    author: str
    """The author of the article."""
    summary: Summary
    """The summary of the article."""
    categories: list[State | str]
    """The list of categories associated with this article."""
    origin: Origin
    """The origin of the article."""

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
            published=datetime.fromtimestamp(data["published"]),
            author=data["author"],
            summary=Summary.from_json(data["summary"]),
            categories=[
                category if id_is_a_folder(category) else State(category)
                for category in data["categories"]
            ],
            origin=Origin.from_json(data["origin"]),
        )


##############################################################################
class Articles(OldList[Article]):
    """Loads and holds a full list of articles."""

    @classmethod
    async def load(cls, session: Session, stream: str | Subscription | Folder, **filters: Any) -> Articles:
        """Load articles for a given stream.

        Args:
            session: The API session object.
            stream: The stream identifier to load from.

        """
        """Load articles for a given stream.

        Args:
            session: The API session object.
            stream: The stream identifier to load from.
            filters: Optional filters for the API.
        """
        if isinstance(stream, (Folder, Subscription)):
            stream = stream.id
        articles: list[Article] = []
        continuation: str | None = ""
        while True:
            result = await session.get(
                "/stream/contents", s=stream, c=continuation, n=1_000, **filters
            )
            articles.extend(
                Article.from_json(article) for article in result.get("items", [])
            )
            if not (continuation := result.get("continuation")):
                break
        return cls(articles)

    @classmethod
    async def load_unread(
        cls, session: Session, stream: str | Subscription | Folder
    ) -> Articles:
        """Load unread articles for a given stream.

        Args:
            session: The API session object.
            stream: The stream identifier to load from.
        """
        return await cls.load(session, stream, xt=State.READ)

    @classmethod
    async def load_new_since(cls, session: Session, stream: str | Subscription | Folder, since: datetime) -> Articles:
        """Load unread articles for a given stream.

        Args:
            session: The API session object.
            stream: The stream identifier to load from.
            since: Time from which to load articles.
        """
        return await cls.load(session, stream, ot=since.timestamp())

### articles.py ends here
