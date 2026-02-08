"""Test for the SubscribeResult."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from oldas.subscriptions import SubscribeResult


##############################################################################
@mark.parametrize(
    "result, expected_result",
    (
        (SubscribeResult("", 1, "", ""), True),
        (SubscribeResult("", 0, "", ""), False),
    ),
)
def test_subscribe(result: SubscribeResult, expected_result: bool) -> None:
    """The various ways of testing for success or failure should work."""
    assert result.succeeded is expected_result
    assert result.failed is not expected_result
    assert bool(result) is expected_result


### test_subscribe_result.py ends here
