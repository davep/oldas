"""Provides a class for getting and holding the user information."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from datetime import datetime, timezone

##############################################################################
# Local imports.
from .session import Session


##############################################################################
@dataclass
class User:
    """TheOldReader user information."""

    user_id: str
    """The user's ID."""
    name: str
    """The user's name."""
    profile_id: str
    """The user's profile ID."""
    email: str
    """The user's email address."""
    is_blogger_user: bool
    """Is the user a Blogger user?"""
    signup_time: datetime
    """The signup time of the user."""
    is_multi_login_enabled: bool
    """Is multi-login enabled?"""
    is_premium: bool
    """Is the user a premium user?"""

    @classmethod
    async def load(cls, session: Session) -> User:
        """Load the current user's details.

        Args:
            session: The API session to use to load the data.

        Returns:
            The user details.
        """
        user = await session.get("user-info")
        return cls(
            user_id=user["userId"],
            name=user["userName"],
            profile_id=user["userProfileId"],
            email=user["userEmail"],
            is_blogger_user=user["isBloggerUser"],
            signup_time=datetime.fromtimestamp(user["signupTimeSec"], timezone.utc),
            is_multi_login_enabled=user["isMultiLoginEnabled"],
            is_premium=user["isPremium"],
        )


### user.py ends here
