"""Provides code for steaming article IDs."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from datetime import datetime, timezone
from typing import Any, AsyncIterator, NamedTuple

##############################################################################
# Local imports.
from .prefixes import Prefix
from .session import Session
from .states import State
from .types import OldList, RawData


##############################################################################
class ArticleID(NamedTuple):
    """Holds an article ID."""

    article_id: str
    """The article ID."""
    direct_stream_ids: list[str]
    """The direct stream IDs."""
    timestamp: datetime
    """The timestamp associated with the article ID."""
    raw: RawData | None = None
    """The raw data from the API."""

    @property
    def full_id(self) -> str:
        """The full, prefixed, ID for the article."""
        return f"{Prefix.ARTICLE}{self.article_id}"

    @classmethod
    def from_json(cls, data: RawData) -> ArticleID:
        """Load the article ID from JSON data.

        Args:
            data: The data to load the article ID from.

        Returns:
            The article ID.
        """
        return cls(
            raw=data,
            article_id=data["id"],
            direct_stream_ids=data["directStreamIds"],
            timestamp=datetime.fromtimestamp(
                int(data["timestampUsec"]) / 1_000_000, timezone.utc
            ),
        )


##############################################################################
class ArticleIDs(OldList[ArticleID]):
    """Loads and holds [article ID][oldas.ArticleID] list."""

    @classmethod
    async def stream(
        cls, session: Session, state: State, **filters: Any
    ) -> AsyncIterator[ArticleID]:
        """Stream [article IDs][oldas.ArticleID].

        Args:
            session: The API session object.
            state: The [`State`][oldas.State] to stream.

        Yields:
            The [article IDs][oldas.ArticleID].
        """
        continuation: str | None = ""
        while True:
            result = await session.get(
                "/stream/items/ids", s=str(state), n=10_000, c=continuation, **filters
            )
            for article_id in (
                ArticleID.from_json(article_id)
                for article_id in result.get("itemRefs", [])
            ):
                yield article_id
            if not (continuation := result.get("continuation")):
                break

    @classmethod
    async def load(cls, session: Session, state: State, **filters: Any) -> ArticleIDs:
        """Load [article IDs][oldas.ArticleID].

        Args:
            session: The API session object.
            state: The [`State`][oldas.State] to stream.
            filters: Any addition filter values.

        Returns:
            The list of matching [article IDs][oldas.ArticleID].
        """
        ids: list[ArticleID] = []
        async for article_id in cls.stream(session, state, **filters):
            ids.append(article_id)
        return cls(ids)

    @classmethod
    async def load_read(cls, session: Session) -> ArticleIDs:
        """Load the list of [IDs][oldas.ArticleID] for all read articles.

        Args:
            session: The API session object.

        Returns:
            The list of read [article IDs][oldas.ArticleID].
        """
        return await cls.load(session, State.READ)

    @classmethod
    async def load_unread(cls, session: Session) -> ArticleIDs:
        """Load the list of [IDs][oldas.ArticleID] for all unread articles.

        Args:
            session: The API session object.

        Returns:
            The list of unread [article IDs][oldas.ArticleID].
        """
        return await cls.load(session, State.READING_LIST, xt=State.READ)


### id_streams.py ends here
