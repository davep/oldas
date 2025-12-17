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
from .exceptions import OldASError, OldASInvalidLogin
from .folders import Folder, Folders
from .session import Session
from .subscriptions import Subscription, Subscriptions
from .unread import Count, Unread

##############################################################################
# Exports.
__all__ = [
    "Count",
    "Folder",
    "Folders",
    "OldASError",
    "OldASInvalidLogin",
    "Session",
    "Subscription",
    "Subscriptions",
    "Unread",
]

### __init__.py ends here
