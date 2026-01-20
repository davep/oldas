"""Provides a class for getting subscription information."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from datetime import datetime, timezone
from typing import NamedTuple

##############################################################################
# Local imports.
from .session import Session
from .types import OldList, RawData


##############################################################################
class Category(NamedTuple):
    """Holds details of a category."""

    id: str
    """The ID for the category."""
    label: str
    """The label for the category."""
    raw: RawData | None = None
    """The raw data from the API."""

    @classmethod
    def from_json(cls, data: RawData) -> Category:
        """Load the category from JSON data.

        Args:
            data: The data to load the category from.

        Returns:
            The category.
        """
        return cls(
            raw=data,
            id=data["id"],
            label=data["label"],
        )


##############################################################################
class Categories(OldList[Category]):
    """Holds a collection of [categories][oldas.subscriptions.Category]."""


##############################################################################
class Subscription(NamedTuple):
    """Holds a subscription."""

    id: str
    """The ID of the subscription."""
    title: str
    """The title of the subscription."""
    sort_id: str
    """The sort ID of the subscription."""
    first_item_time: datetime
    """The time of the first item."""
    url: str
    """The URL of the subscription."""
    html_url: str
    """The HTML URL of the subscription."""
    categories: Categories
    """The categories for the subscription."""
    raw: RawData | None = None
    """The raw data from the API."""

    @classmethod
    def from_json(cls, data: RawData) -> Subscription:
        """Load the subscription from JSON data.

        Args:
            data: The data to load the subscription from.

        Returns:
            The subscription.
        """
        return cls(
            raw=data,
            id=data["id"],
            title=data["title"],
            sort_id=data["sortid"],
            first_item_time=datetime.fromtimestamp(
                int(data["firstitemmsec"]) / 1_000, timezone.utc
            ),
            url=data["url"],
            html_url=data["htmlUrl"],
            categories=Categories(
                Category.from_json(category) for category in data["categories"]
            ),
        )


##############################################################################
class SubscribeResult(NamedTuple):
    """Class that holds the request of adding a subscription."""

    query: str
    """The query that was performed."""
    number_of_results: int
    """The number of requests from the query to add."""
    stream_id: str | None
    """The stream ID if the subscription took place."""
    error: str | None
    """The reason why the subscribe failed, if it did."""
    raw: RawData | None = None
    """The raw data from the API."""

    @classmethod
    def from_json(cls, data: RawData) -> SubscribeResult:
        """Load the subscribe result from JSON data.

        Args:
            data: The data to load the subscribe result from.

        Returns:
            The result of making the subscribe request.
        """
        return cls(
            raw=data,
            query=data["query"],
            number_of_results=data["numResults"],
            stream_id=data.get("streamId"),
            error=data.get("error"),
        )

    @property
    def failed(self) -> bool:
        """Did the request to subscribe fail?"""
        return self.number_of_results == 0


##############################################################################
class Subscriptions(OldList[Subscription]):
    """Loads and holds the full list of [subscriptions][oldas.Subscription]."""

    @classmethod
    async def load(cls, session: Session) -> Subscriptions:
        """Load the subscriptions.

        Args:
            session: The API session object.

        Returns:
            A list of subscriptions.
        """
        return cls(
            Subscription.from_json(subscription)
            for subscription in (await session.get("subscription/list"))[
                "subscriptions"
            ]
        )

    @staticmethod
    async def add(session: Session, feed: str) -> SubscribeResult:
        """Add a subscription.

        Args:
            session: The API session object.
            feed: The feed to subscribe to.

        Returns:
            A [`SubscribeResult`][oldas.subscriptions.SubscribeResult].
        """
        return SubscribeResult.from_json(
            await session.post("subscription/quickadd", quickadd=feed)
        )


### subscriptions.py ends here
