"""Provide the JSONDict class for holding JSON object data."""

from __future__ import annotations

__all__: list[str] = ["JSONDict"]

from collections import abc
from typing import Any, Self

import datahold
from frozendict import frozendict

from .._utils.funcs import SupportsKeysAndGetitem, gendict
from .JSONCollection import JSONCollection


class JSONDict(datahold.HoldDict[str, Any], JSONCollection[Any]):

    __slots__ = ()

    def _dump(self: Self, /) -> dict[str, Any]:
        "Return the held dictionary data as a dict."
        return dict(gendict(self._data, dump=True))

    @property
    def data(self: Self, /) -> frozendict[str, Any]:
        "Return the held dictionary data."
        return self._data

    @data.setter
    def data(
        self: Self,
        data_: (
            SupportsKeysAndGetitem[Any]
            | abc.Iterable[tuple[abc.Hashable, Any]]
        ),
        /,
    ) -> None:
        "Set the held dictionary data from keys and values."
        self._data = frozendict(gendict(data_, dump=False))
