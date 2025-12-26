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
from ._prefixes import Prefix, id_is_a_feed, id_is_a_folder
from ._states import State
from .articles import Article, Articles
from .exceptions import OldASError, OldASInvalidLogin
from .folders import Folder, Folders
from .session import Session
from .subscriptions import Subscription, Subscriptions
from .unread import Count, Counts, Unread

##############################################################################
# Exports.
__all__ = [
    "Article",
    "Articles",
    "Count",
    "Counts",
    "Folder",
    "Folders",
    "id_is_a_feed",
    "id_is_a_folder",
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
