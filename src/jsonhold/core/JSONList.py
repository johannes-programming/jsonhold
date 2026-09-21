"""Provide the JSONList class for holding JSON array data."""

from __future__ import annotations

__all__: list[str] = ["JSONList"]

import io
import json
from collections import abc
from typing import Any, Self

import datahold

from .._utils.funcs import genlist


class JSONList(datahold.HoldList[Any]):

    __slots__ = ()

    @property
    def data(self: Self, /) -> tuple[Any, ...]:
        "Return the held list data as tuple."
        return self._data

    @data.setter
    def data(self: Self, value: abc.Iterable[Any], /) -> None:
        "Set the held list data from an iterable."
        self._data = tuple(genlist(value, dump=False))

    def dump(self: Self, stream: io.BufferedWriter, /, **kwargs: Any) -> None:
        "Dump the data into a text stream."
        json.dump(list(genlist(self._data, dump=True)), stream, **kwargs)

    def dumpintofile(self: Self, file: str, /, **kwargs: Any) -> None:
        "Dump the data into a UTF-8 encoded JSON file."
        with open(file, "w", encoding="utf-8") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, /, **kwargs: Any) -> str:
        "Dump the data as a string."
        return json.dumps(list(genlist(self._data, dump=True)), **kwargs)
