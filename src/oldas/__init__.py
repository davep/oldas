"""TheOldReader API async client library."""

##############################################################################
# Python imports.
from importlib.metadata import version

######################################################################
# Main library information.
__author__ = "Dave Pearson"
__copyright__ = "Copyright 2025, Dave Pearson"
__credits__ = ["Dave Pearson"]
__maintainer__ = "Dave Pearson"
__email__ = "davep@davep.org"
__version__: str = version("oldas")
__licence__ = "MIT"

##############################################################################
# Local imports.
from .articles import Article, Articles
from .exceptions import OldASError, OldASInvalidLogin
from .folders import Folder, Folders
from .id_streams import ArticleID, ArticleIDs
from .prefixes import Prefix, id_is_a_feed, id_is_a_folder, id_is_an_article
from .session import Session
from .states import State
from .subscriptions import Subscription, Subscriptions
from .unread import Count, Counts, Unread

##############################################################################
# Exports.
__all__ = [
    "Article",
    "ArticleID",
    "ArticleIDs",
    "Articles",
    "Count",
    "Counts",
    "Folder",
    "Folders",
    "id_is_a_feed",
    "id_is_a_folder",
    "id_is_an_article",
    "OldASError",
    "OldASInvalidLogin",
    "Prefix",
    "Session",
    "State",
    "Subscription",
    "Subscriptions",
    "Unread",
]

### __init__.py ends here
