"""Provide the JSONList class for holding JSON array data."""

from __future__ import annotations

__all__: list[str] = ["JSONList"]

import json
from collections.abc import Iterable
from typing import Any, Self

import datahold

from .._utils.funcs import genlist


class JSONList(datahold.HoldList[Any]):
    @property
    def data(self: Self) -> tuple[Any, ...]:
        "Return the held list data as tuple."
        return self._data

    @data.setter
    def data(self: Self, value: Iterable[Any]) -> None:
        "Set the held list data from an iterable."
        self._data = tuple(genlist(value, dump=False))

    def dump(self: Self, stream: Any, /, **kwargs: Any) -> None:
        "Dump the data into a text stream."
        json.dump(list(genlist(self._data, dump=True)), stream, **kwargs)

    def dumpintofile(self: Self, file: str, /, **kwargs: Any) -> None:
        "Dump the data into a UTF-8 encoded JSON file."
        with open(file, "w", encoding="utf-8") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, **kwargs: Any) -> str:
        "Dump the data as a string."
        return json.dumps(list(genlist(self._data, dump=True)), **kwargs)

    @classmethod
    def load(cls: type[Self], stream: Any, /, **kwargs: Any) -> Self:
        "Load a JSON array from a text stream."
        value: Any = json.load(stream, **kwargs)
        if not isinstance(value, list):
            raise TypeError("JSONList can only load a JSON array")
        return cls(value)

    @classmethod
    def loadfromfile(cls: type[Self], file: str, /, **kwargs: Any) -> Self:
        "Load a JSON array from a UTF-8 encoded file."
        with open(file, "r", encoding="utf-8") as stream:
            return cls.load(stream, **kwargs)

    @classmethod
    def loads(cls: type[Self], string: str, /, **kwargs: Any) -> Self:
        "Load a JSON array from a string."
        value: Any = json.loads(string, **kwargs)
        if not isinstance(value, list):
            raise TypeError("JSONList can only load a JSON array")
        return cls(value)
