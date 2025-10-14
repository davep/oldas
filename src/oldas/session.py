"""Provides a class for getting and managing a login session."""

##############################################################################
from typing import Any, Final, Self

##############################################################################
# Httpx imports.
from httpx import AsyncClient, RequestError, HTTPStatusError

##############################################################################
# Local imports.
from . import __version__
from .exceptions import OldASError

##############################################################################
class Session:
    """Class for handling a TheOldReader login session."""

    _LOGIN: Final[str] = "https://theoldreader.com/accounts/ClientLogin"
    """The URL of the endpoint used to log in."""

    _API: Final[str] = "https://theoldreader.com/reader/api/0/"
    """The URL of the API endpoint."""

    _USER_AGENT: Final[str] = f"oldas v{__version__} (https://github.com/davep/oldas)"
    """The user agent to use for the library."""

    def __init__(self, client: str, auth_code: str | None = None) -> None:
        """Initialise the object.

        Args:
            client: The name of the client that is logging in.
            auth_code: Optional authorization code to resume a session.

        Note:
            The `client` should be a unique name you give your client
            application that is using this library.
        """
        self._client = client
        """The name of the client to log in as."""
        self._auth_code = auth_code
        """The auth code."""

    @property
    def logged_in(self) -> bool:
        """Are we logged in?"""
        return self._auth_code is not None

    async def login(self, user: str, password: str) -> Self:
        """Log into TheOldReader.

        Args:
            user: The user name to log in with.
            password: The password to log in with.

        Returns:
            Self.

        Raises:
            OldASError: If there was an error connecting or logging in.
        """
        if self._auth_code is None:
            async with AsyncClient() as client:
                try:
                    response = await client.post(
                        self._LOGIN,
                        json={
                            "accountType": "HOSTED_OR_GOOGLE",
                            "client": self._client,
                            "Email": user,
                            "Passwd": password,
                            "service": "reader",
                            "output": "json",
                            "user-agent": self._USER_AGENT,
                        }
                    )
                except RequestError as error:
                    raise OldASError(str(error)) from None
                try:
                    response.raise_for_status()
                except HTTPStatusError as error:
                    raise OldASError(str(error)) from None
                self._auth_code = response.json().get("Auth")
        return self

    def logout(self) -> Self:
        """Log out of the TheOldReader."""
        self._auth_code = None
        return self

    def _must_be_logged_in(self) -> None:
        """Checks if we're logged in and raises an error if not."""
        if not self.logged_in:
            raise OldASError("API call made but not logged in")

    async def get(self, url: str) -> dict[str, Any]:
        """Make a GET call to the API.

        Args:
            url: The URL to call.

        Returns:
            A dictionary that is the JSON data.
        """
        self._must_be_logged_in()
        async with AsyncClient() as client:
            response = await client.get(
                f"{self._API}{url}",
                headers={
                    "Authorization": f"GoogleLogin auth={self._auth_code}"
                },
                params={"output": "json", "user-agent": self._USER_AGENT}
            )
            return response.json()

### session.py ends here
