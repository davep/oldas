"""Provides exception classes for the library."""


##############################################################################
class OldASError(Exception):
    """Base exception for exceptions raised by the library."""


##############################################################################
class OldASInvalidLogin(OldASError):
    """Exception thrown if the login failed."""


##############################################################################
class OldASLoginNeeded(OldASError):
    """Exception thrown when a call is made when a login is needed.

    Note:
        This exception might indicate that either no login has happened yet,
        or it might indicate that a previous login has gone stale and a
        fresh one should take place.
    """


### exceptions.py ends here
