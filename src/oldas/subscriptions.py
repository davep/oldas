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


### subscriptions.py ends here
