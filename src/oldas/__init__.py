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
__version__ = version("oldas")
__licence__ = "MIT"

##############################################################################
# Local imports.
from .exceptions import OldASError

##############################################################################
# Exports.
__all__ = ["OldASError"]

### __init__.py ends here
