"""Provides a class for getting and managing a login session."""

##############################################################################
from typing import Any, Awaitable, Final, Self

##############################################################################
# Httpx imports.
import httpx
from httpx import AsyncClient, HTTPStatusError, ReadTimeout, RequestError, Response

##############################################################################
# Local imports.
from . import __version__
from ._types import RawData
from .exceptions import OldASError, OldASInvalidLogin, OldASLoginNeeded


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

    @property
    def auth_code(self) -> str | None:
        """The auth code, if we are logged in, else `None`."""
        return self._auth_code

    async def _call(self, call: Awaitable[Response]) -> Response:
        """Make a call out to the API.

        Args:
            call: The call to make.

        Returns:
            The response.

        Raises:
            OldASError: If there was an error connecting or logging in.
        """
        try:
            response = await call
        except ReadTimeout:
            raise OldASError("Timeout while talking to TheOldReader API")
        except RequestError as error:
            raise OldASError(str(error)) from None
        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            if error.response.status_code == httpx.codes.UNAUTHORIZED:
                raise OldASLoginNeeded("The current token is not valid") from None
            if error.response.status_code == httpx.codes.FORBIDDEN:
                raise OldASInvalidLogin(str(error)) from None
            raise OldASError(str(error)) from None
        return response

    @property
    def _headers(self) -> dict[str, str]:
        """The standard headers for a call to TheOldReader."""
        return {
            "user-agent": self._USER_AGENT,
        } | (
            {"Authorization": f"GoogleLogin auth={self._auth_code}"}
            if self.logged_in
            else {}
        )

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
                self._auth_code = (
                    (
                        await self._call(
                            client.post(
                                self._LOGIN,
                                json={
                                    "accountType": "HOSTED_OR_GOOGLE",
                                    "client": self._client,
                                    "Email": user,
                                    "Passwd": password,
                                    "service": "reader",
                                    "output": "json",
                                },
                                headers=self._headers,
                            )
                        )
                    )
                    .json()
                    .get("Auth")
                )
        return self

    def logout(self) -> Self:
        """Log out of the TheOldReader."""
        self._auth_code = None
        return self

    def _must_be_logged_in(self) -> None:
        """Checks if we're logged in and raises an error if not."""
        if not self.logged_in:
            raise OldASLoginNeeded("API call made but not logged in")

    @staticmethod
    def _verify_raw(data: Any) -> RawData:
        """Verify that the given data is of the type we expect.

        Args:
            data: The data that was received.

        Returns:
            The verified data, of the expected type.
        """
        if isinstance(data, dict):
            return data
        raise OldASError("Unexpected data type received from TheOldReader API")

    async def get(self, url: str, **params: Any) -> RawData:
        """Make a GET call to the API.

        Args:
            url: The URL to call.
            params: Any extra parameters that need to be passed.

        Returns:
            A dictionary that is the JSON data.

        Raises:
            OldASError: If there was an error connecting or logging in.
        """
        self._must_be_logged_in()
        # TODO: Make this timeout configurable.
        async with AsyncClient(timeout=60) as client:
            return self._verify_raw(
                (
                    await self._call(
                        client.get(
                            f"{self._API}{url}",
                            headers=self._headers,
                            params={**params, "output": "json"},
                        )
                    )
                ).json()
            )


### session.py ends here
