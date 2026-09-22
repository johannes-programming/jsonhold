"""Provide the JSONList class for holding JSON array data."""

from __future__ import annotations

__all__: list[str] = ["JSONList"]

from collections import abc
from typing import Any, Self

import datahold

from .._utils.funcs import genlist
from .JSONCollection import JSONCollection

class JSONList(datahold.HoldList[Any], JSONCollection[Any]):

    __slots__ = ()

    def _dump(self: Self, /) -> list[Any]:
        "Return the held list data as a list."
        return list(genlist(self._data, dump=True))

    @property
    def data(self: Self, /) -> tuple[Any, ...]:
        "Return the held list data as tuple."
        return self._data

    @data.setter
    def data(self: Self, data_: abc.Iterable[Any], /) -> None:
        "Set the held list data from an iterable."
        self._data = tuple(genlist(data_, dump=False))
