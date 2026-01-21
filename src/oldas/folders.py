"""Provides a class for loading up the folders."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import NamedTuple

##############################################################################
# Local imports.
from .prefixes import Prefix, id_is_a_folder
from .session import Session
from .types import OldList, RawData


##############################################################################
class Folder(NamedTuple):
    """Folder information class."""

    id: str
    """The ID of the folder."""
    sort_id: str
    """The sort ID of the folder."""
    raw: RawData | None = None
    """The raw data from the API."""

    @property
    def name(self) -> str:
        """The name of the folder."""
        return self.id.removeprefix(Prefix.FOLDER)

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
    """Load the [folder][oldas.Folder] list from TheOldReader."""

    @classmethod
    async def load(cls, session: Session) -> Folders:
        """Load the folders.

        Args:
            session: The API session object.

        Returns:
            A list of [folders][oldas.Folder].
        """
        return cls(
            Folder.from_json(folder)
            for folder in (await session.get("tag/list"))["tags"]
            if id_is_a_folder(folder.get("id", ""))
        )

    @staticmethod
    async def rename(
        session: Session, rename_from: str | Folder, rename_to: str
    ) -> bool:
        """Rename a folder on the server.

        Args:
            session: The API session object.
            rename_from: The folder that is to be renamed.
            rename_to: The new name for the folder.

        Returns:
            [`True`][True] if the rename worked, [`False`][False] if not.

        Notes:
            `rename_from` and `rename_to` can have or be missing the prefix
            [`Prefix.FOLDER`][oldas.prefixes.Prefix.FOLDER]; this method
            will handle either case and do the right thing.
        """
        if isinstance(rename_from, Folder):
            rename_from = rename_from.id
        if not id_is_a_folder(rename_from):
            rename_from = f"{Prefix.FOLDER}{rename_from}"
        if not id_is_a_folder(rename_to):
            rename_to = f"{Prefix.FOLDER}{rename_to}"
        return await session.post_ok("rename-tag", s=rename_from, dest=rename_to)


### folders.py ends here
