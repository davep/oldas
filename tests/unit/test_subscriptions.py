"""Tests for code relating to the subscriptions."""

##############################################################################
# Local imports.
from oldas import Subscription, Subscriptions

##############################################################################
TEST_SUBSCRIPTIONS = Subscriptions(
    [
        Subscription.from_json(
            {
                "id": "1",
                "title": "z",
                "sortid": "",
                "firstitemmsec": 0,
                "url": "https://example.com/",
                "htmlUrl": "https://example.com/",
                "categories": [],
            }
        ),
        Subscription.from_json(
            {
                "id": "1",
                "title": "a",
                "sortid": "",
                "firstitemmsec": 0,
                "url": "https://example.com/",
                "htmlUrl": "https://example.com/",
                "categories": [],
            }
        ),
    ]
)


##############################################################################
def test_sort_subscriptions() -> None:
    """Subscriptions should sort by title."""
    assert [subscription.title for subscription in TEST_SUBSCRIPTIONS] == ["z", "a"]
    assert [subscription.title for subscription in sorted(TEST_SUBSCRIPTIONS)] == [
        "a",
        "z",
    ]


### test_subscriptions.py ends here
