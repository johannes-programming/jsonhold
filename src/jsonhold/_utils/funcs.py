"""Provide generator and value conversion utilities for JSON data."""

from __future__ import annotations

__all__: list[str] = ["gendict", "genlist", "getvalue"]

import operator
from collections.abc import Generator, Hashable, Iterable, Mapping, Sequence
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Protocol, Self, overload

if TYPE_CHECKING:
    from ..core.JSONDict import JSONDict
    from ..core.JSONList import JSONList


class SupportsKeysAndGetitem[Value](Protocol):
    "Protocol for objects that support keys() and __getitem__()."

    def keys(self: Self, /) -> Iterable[Hashable]: ...

    def __getitem__(self: Self, key: Hashable, /) -> Value: ...


def gendict(
    data: Any,
    /,
    *,
    dump: bool = False,
) -> Generator[tuple[str, Any], None, None]:
    "Generate string-keyed items from mapping data for JSON."
    x: Hashable
    y: Any
    for x, y in dict(data).items():
        yield str(x), getvalue(y, dump=dump)


def genlist(
    data: Iterable[Any], /, *, dump: bool = False
) -> Generator[Any, None, None]:
    "Generate processed items from iterable data for JSON."
    x: Any
    for x in data:
        yield getvalue(x, dump=dump)


@overload
def getvalue(value: None, /, *, dump: bool = False) -> None: ...
@overload
def getvalue(
    value: Mapping[Hashable, Any], /, *, dump: bool = False
) -> JSONDict | dict[str, Any]: ...
@overload
def getvalue(value: str, /, *, dump: bool = False) -> str: ...
@overload
def getvalue(
    value: Sequence[Any], /, *, dump: bool = False
) -> JSONList | list[Any]: ...
@overload
def getvalue(value: bool, /, *, dump: bool = False) -> bool: ...
@overload
def getvalue(value: int, /, *, dump: bool = False) -> int: ...
@overload
def getvalue(value: Decimal | float, /, *, dump: bool = False) -> Decimal: ...
def getvalue(value: Any, /, *, dump: bool = False) -> Any:
    "Return a JSON value."
    if value is None:
        return None
    if isinstance(value, Mapping):
        if dump:
            return dict(gendict(value, dump=True))
        from ..core.JSONDict import JSONDict

        return JSONDict(value)
    if isinstance(value, str):
        return str(value)
    if isinstance(value, Sequence):
        if dump:
            return list(genlist(value, dump=True))
        from ..core.JSONList import JSONList

        return JSONList(value)
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, int):
        return operator.index(value)
    return Decimal(value)
