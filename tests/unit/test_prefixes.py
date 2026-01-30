"""Tests relating to prefixes."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from oldas import Folders, Subscriptions, id_is_a_feed, id_is_a_folder


##############################################################################
@mark.parametrize(
    "test_id, expected_result",
    (
        (Folders.full_id("test"), True),
        (Subscriptions.full_id("test"), False),
    ),
)
def test_is_a_folder(test_id: str, expected_result: bool) -> None:
    """We should be able to test for a folder ID."""
    assert id_is_a_folder(test_id) is expected_result


##############################################################################
@mark.parametrize(
    "test_id, expected_result",
    (
        (Folders.full_id("test"), False),
        (Subscriptions.full_id("test"), True),
    ),
)
def test_is_a_feed(test_id: str, expected_result: bool) -> None:
    """We should be able to test for a feed ID."""
    assert id_is_a_feed(test_id) is expected_result


### test_prefixes.py ends here
