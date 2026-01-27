"""Tests for the code relating to folders."""

##############################################################################
# Local imports.
from oldas import Folder, Folders
from oldas.prefixes import Prefix

##############################################################################
TEST_FOLDERS = Folders(
    [
        Folder.from_json({"id": f"{Prefix.FOLDER}z", "sortid": ""}),
        Folder.from_json({"id": f"{Prefix.FOLDER}a", "sortid": ""}),
    ]
)


##############################################################################
def test_sort_folders() -> None:
    """Folders should sort by name."""
    assert [folder.name for folder in TEST_FOLDERS] == ["z", "a"]
    assert [folder.name for folder in sorted(TEST_FOLDERS)] == ["a", "z"]


### test_folders.py ends here
