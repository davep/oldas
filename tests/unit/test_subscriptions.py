"""Tests for code relating to the subscriptions."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from oldas import Folder, Folders, Subscription, Subscriptions
from oldas.prefixes import Prefix
from oldas.subscriptions import Category

##############################################################################
RAW_TEST_CATEGORY = {"id": Folders.full_id("Test"), "label": "Test"}
TEST_CATEGORY = Category.from_json(RAW_TEST_CATEGORY)

##############################################################################
TEST_FOLDER = Folder.from_json({"id": Folders.full_id("Test"), "sortid": ""})


##############################################################################
TEST_SUBSCRIPTIONS = Subscriptions(
    [
        Subscription.from_json(
            {
                "id": f"{Prefix.FEED}foo",
                "title": "Z",
                "sortid": "",
                "firstitemmsec": 0,
                "url": "https://example.com/",
                "htmlUrl": "https://example.com/",
                "categories": [RAW_TEST_CATEGORY],
            }
        ),
        Subscription.from_json(
            {
                "id": f"{Prefix.FEED}bar",
                "title": "a",
                "sortid": "",
                "firstitemmsec": 0,
                "url": "https://example.com/",
                "htmlUrl": "https://example.com/",
                "categories": [RAW_TEST_CATEGORY],
            }
        ),
    ]
)


##############################################################################
@mark.parametrize(
    "data, result",
    (
        (TEST_CATEGORY, True),
        (TEST_CATEGORY.id, True),
        (TEST_FOLDER, True),
        (TEST_FOLDER.id, True),
        ("unknown", False),
    ),
)
def test_subscription_categories_contains(
    data: str | Category | Folder, result: bool
) -> None:
    """We should be able to `in` test categories of a subscription."""
    assert (data in TEST_SUBSCRIPTIONS[0].categories) is result


### test_subscriptions.py ends here
