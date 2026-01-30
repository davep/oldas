"""Provides a class for getting subscription information."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from datetime import datetime, timezone

##############################################################################
# Local imports.
from .folders import Folder, Folders
from .prefixes import Prefix, id_is_a_feed, id_is_a_folder
from .session import Session
from .types import OldList, RawData


##############################################################################
@dataclass(frozen=True)
class Category:
    """Holds details of a category."""

    id: str
    """The ID for the category."""
    label: str
    """The label for the category."""

    @classmethod
    def from_json(cls, data: RawData) -> Category:
        """Load the category from JSON data.

        Args:
            data: The data to load the category from.

        Returns:
            The category.
        """
        return cls(
            id=data["id"],
            label=data["label"],
        )


##############################################################################
class Categories(OldList[Category]):
    """Holds a collection of [categories][oldas.subscriptions.Category]."""

    def __contains__(self, data: Category | Folder | str) -> bool:
        """Check if some data is `in` the categories.

        Args:
            data: The category, folder or string to look for.

        Returns:
            [`True`][True] if the data was found, [`False`][False] if not.
        """
        if isinstance(data, (Category, Folder)):
            data = data.id
        return any(category.id == data for category in self)


##############################################################################
@dataclass(frozen=True)
class Subscription:
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

    @classmethod
    def from_json(cls, data: RawData) -> Subscription:
        """Load the subscription from JSON data.

        Args:
            data: The data to load the subscription from.

        Returns:
            The subscription.
        """
        return cls(
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

    @property
    def folder_id(self) -> str | None:
        """The ID of the folder that this subscription belongs to, or [`None`][None] if it doesn't.

        Note:
            According to the API documentation it would appear that a
            subscription could be a member of multiple folders. Note that
            this property is the ID of the first folder that could be found
            amongst the
            [categories][oldas.subscriptions.Subscription.categories].
        """
        return next(
            (
                category.id
                for category in self.categories
                if id_is_a_folder(category.id)
            ),
            None,
        )


##############################################################################
@dataclass(frozen=True)
class SubscribeResult:
    """Class that holds the request of adding a subscription."""

    query: str
    """The query that was performed."""
    number_of_results: int
    """The number of requests from the query to add."""
    stream_id: str | None
    """The stream ID if the subscription took place."""
    error: str | None
    """The reason why the subscribe failed, if it did."""

    @classmethod
    def from_json(cls, data: RawData) -> SubscribeResult:
        """Load the subscribe result from JSON data.

        Args:
            data: The data to load the subscribe result from.

        Returns:
            The result of making the subscribe request.
        """
        return cls(
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

        Notes:
            The `feed` will normally be the URL of the feed to subscribe to.
        """
        return SubscribeResult.from_json(
            await session.post("subscription/quickadd", quickadd=feed)
        )

    @staticmethod
    def full_id(subscription: str | Subscription) -> str:
        """Get the full ID for a given subscription.

        Args:
            subscription: The subscription to get the full ID for.

        Returns:
            The full ID for the subscription.
        """
        if isinstance(subscription, Subscription):
            subscription = subscription.id
        return (
            subscription
            if id_is_a_feed(subscription)
            else f"{Prefix.FEED}{subscription}"
        )

    @classmethod
    async def rename(
        cls, session: Session, subscription: str | Subscription, new_name: str
    ) -> bool:
        """Rename a subscription.

        Args:
            session: The API session object.
            subscription: The subscription to rename.
            new_name: The new name for the subscription.

        Returns:
            [`True`][True] if the rename call worked, [`False`][False] if not.

        Note:
            The `subscription` can either be a string that is the ID of a feed, or
            it can be a [`Subscription`][oldas.Subscription] object.
        """
        return await session.post_ok(
            "subscription/edit", ac="edit", s=cls.full_id(subscription), t=new_name
        )

    @classmethod
    async def remove(cls, session: Session, subscription: str | Subscription) -> bool:
        """Remove a subscription.

        Args:
            session: The API session object.
            subscription: The subscription to unsubscribe.

        Returns:
            [`True`][True] if the unsubscribe call worked, [`False`][False] if not.

        Note:
            The `subscription` can either be a string that is the ID of a feed, or
            it can be a [`Subscription`][oldas.Subscription] object.
        """
        return await session.post_ok(
            "subscription/edit", ac="unsubscribe", s=cls.full_id(subscription)
        )

    @classmethod
    async def move(
        cls,
        session: Session,
        subscription: str | Subscription,
        target_folder: str | Folder | None = None,
    ) -> bool:
        """Move a subscription to a different folder.

        Args:
            session: The API session object.
            subscription: The subscription to move.
            target_folder: The folder to move the subscription to.

        Returns:
            [`True`][True] if the move call worked, [`False`][False] if not.

        Note:
            If `target_folder` is omitted, is [`None`][None], or is an empty
            [string][str], the subscription will be moved to the top-level
            default folder.
        """
        if isinstance(target_folder, str):
            target_folder = target_folder.strip()
        operation = (
            {"r": "remove"}
            if not target_folder
            else {"a": Folders.full_id(target_folder)}
        )
        return await session.post_ok(
            "subscription/edit", ac="edit", s=cls.full_id(subscription), **operation
        )


### subscriptions.py ends here
