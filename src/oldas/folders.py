"""Provides a class for loading up the folders."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import Any, NamedTuple

##############################################################################
# Local imports.
from .session import Session


##############################################################################
class Folder(NamedTuple):
    """Folder information class."""

    id: str
    """The ID of the folder."""
    sort_id: str
    """The sort ID of the folder."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Folder:
        """Load the folder from JSON data.

        Args:
            data: The data to load the folder from.

        Returns:
            The folder information.
        """
        return Folder(
            id=data["id"],
            sort_id=data["sortid"],
        )


##############################################################################
class Folders:
    """Load the folder list from TheOldReader."""

    @classmethod
    async def load(cls, session: Session) -> list[Folder]:
        """Load the folders.

        Args:
            session: The API session object.

        Returns:
            A list of folders.
        """
        return [
            Folder.from_json(folder)
            for folder in (await session.get("tag/list"))["tags"]
        ]


### folders.py ends here
