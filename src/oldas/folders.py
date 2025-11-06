"""Provides a class for loading up the folders."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import NamedTuple

##############################################################################
# Local imports.
from ._types import OldList, RawData
from .session import Session


##############################################################################
class Folder(NamedTuple):
    """Folder information class."""

    raw: RawData
    """The raw data from the API."""
    id: str
    """The ID of the folder."""
    sort_id: str
    """The sort ID of the folder."""

    @classmethod
    def from_json(cls, data: RawData) -> Folder:
        """Load the folder from JSON data.

        Args:
            data: The data to load the folder from.

        Returns:
            The folder information.
        """
        return Folder(
            raw=data,
            id=data["id"],
            sort_id=data["sortid"],
        )


##############################################################################
class Folders(OldList[Folder]):
    """Load the folder list from TheOldReader."""

    @classmethod
    async def load(cls, session: Session) -> Folders:
        """Load the folders.

        Args:
            session: The API session object.

        Returns:
            A list of folders.
        """
        return cls(
            Folder.from_json(folder)
            for folder in (await session.get("tag/list"))["tags"]
        )


### folders.py ends here
