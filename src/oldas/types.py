"""Types used across the library."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    Iterator,
    TypeAlias,
    TypeVar,
    overload,
)

##############################################################################
RawData: TypeAlias = dict[str, Any]
"""Type of raw data that comes from TheOldReader."""

##############################################################################
OldData = TypeVar("OldData")
"""Type used in the OldSequence generic wrapper."""


##############################################################################
class OldList(Generic[OldData]):
    """Base class for classes that wrap a list of data."""

    def __init__(self, data: Iterable[OldData] | None = None) -> None:
        """Initialise the OldList object.

        Args:
            data: The initial data to wrap.
        """
        self._data: list[OldData] = list(data or [])
        """The data we're wrapping around."""

    if TYPE_CHECKING:

        @overload
        def __getitem__(self, index: int) -> OldData: ...
        @overload
        def __getitem__(self, index: slice) -> OldList[OldData]: ...

    def __getitem__(self, index: int | slice) -> OldData | OldList[OldData]:
        return (
            OldList[OldData](self._data[index])
            if isinstance(index, slice)
            else self._data[index]
        )

    def __len__(self) -> int:
        return len(self._data)

    def __length_hint__(self) -> int:
        return len(self)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __contains__(self, data: OldData) -> bool:
        return data in self._data

    def __iter__(self) -> Iterator[OldData]:
        return iter(self._data)

    def __repr__(self) -> str:
        return repr(self._data)


### types.py ends here
