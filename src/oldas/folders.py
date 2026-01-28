"""Provides a class for loading up the folders."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Local imports.
from .prefixes import Prefix, id_is_a_folder
from .session import Session
from .types import OldList, RawData


##############################################################################
@dataclass(frozen=True)
class Folder:
    """Folder information class."""

    id: str
    """The ID of the folder."""
    sort_id: str
    """The sort ID of the folder."""

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
    def full_id(folder: str | Folder) -> str:
        """Turn something that identifies a folder into a full folder ID.

        Args:
            folder: The folder to get the ID from.

        Returns:
            The full prefixed folder ID.
        """
        if isinstance(folder, Folder):
            folder = folder.id
        return folder if id_is_a_folder(folder) else f"{Prefix.FOLDER}{folder}"

    @classmethod
    async def rename(
        cls, session: Session, rename_from: str | Folder, rename_to: str
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
        return await session.post_ok(
            "rename-tag", s=cls.full_id(rename_from), dest=cls.full_id(rename_to)
        )

    @classmethod
    async def remove(cls, session: Session, folder: str | Folder) -> bool:
        """Remove the given folder from the server.

        Args:
            session: The API session object.
            folder: The folder that is to be removed.

        Returns:
            [`True`][True] if the folder was removed, [`False`][False] if not.

        Notes:
            `folder` can have or be missing the prefix
            [`Prefix.FOLDER`][oldas.prefixes.Prefix.FOLDER]; this method
            will handle either case and do the right thing.
        """
        return await session.post_ok("disable-tag", s=cls.full_id(folder))


### folders.py ends here
