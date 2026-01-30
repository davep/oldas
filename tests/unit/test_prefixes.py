"""Tests relating to prefixes."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from oldas import (
    Articles,
    Folders,
    Subscriptions,
    id_is_a_feed,
    id_is_a_folder,
    id_is_an_article,
)


##############################################################################
@mark.parametrize(
    "test_id, expected_result",
    (
        (Folders.full_id("test"), True),
        (Subscriptions.full_id("test"), False),
        (Articles.full_id("test"), False),
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
        (Articles.full_id("test"), False),
    ),
)
def test_is_a_feed(test_id: str, expected_result: bool) -> None:
    """We should be able to test for a feed ID."""
    assert id_is_a_feed(test_id) is expected_result


##############################################################################
@mark.parametrize(
    "test_id, expected_result",
    (
        (Folders.full_id("test"), False),
        (Subscriptions.full_id("test"), False),
        (Articles.full_id("test"), True),
    ),
)
def test_is_an_article(test_id: str, expected_result: bool) -> None:
    """We should be able to test for an article ID."""
    assert id_is_an_article(test_id) is expected_result


### test_prefixes.py ends here
