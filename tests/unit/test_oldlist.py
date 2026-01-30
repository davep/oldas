"""Tests for OldList."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from oldas.types import OldList


##############################################################################
class NumberList(OldList[int]):
    """A list for holding numbers."""


##############################################################################
@mark.parametrize(
    "old_list, expected_length",
    (
        (NumberList(), 0),
        (NumberList([]), 0),
        (NumberList([1]), 1),
        (NumberList(range(100)), 100),
    ),
)
def test_len(old_list: NumberList, expected_length: int) -> None:
    """The `len` of the list should work as expected."""
    assert len(NumberList(old_list)) == expected_length


##############################################################################
@mark.parametrize(
    "old_list, expected",
    (
        (NumberList(), False),
        (NumberList([]), False),
        (NumberList([1]), True),
        (NumberList(range(100)), True),
    ),
)
def test_bool(old_list: NumberList, expected: bool) -> None:
    """The `bool` of the list should work as expected."""
    assert bool(NumberList(old_list)) is expected


##############################################################################
@mark.parametrize(
    "old_list, expected",
    (
        (NumberList(), False),
        (NumberList([]), False),
        (NumberList([23]), True),
        (NumberList([0, 23, 50]), True),
        (NumberList(range(100)), True),
    ),
)
def test_is_in(old_list: OldList, expected: bool) -> None:
    """The `in` test should work as expected."""
    assert (23 in old_list) is expected


### test_oldlist.py ends here
