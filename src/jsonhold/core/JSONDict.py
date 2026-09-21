"""Provide the JSONDict class for holding JSON object data."""

from __future__ import annotations

__all__: list[str] = ["JSONDict"]

import json
from collections.abc import Iterable, Mapping
from typing import Any, Self

import datahold
from datahold.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem
from frozendict import frozendict

from .._utils.funcs import gendict


class JSONDict(datahold.HoldDict[str, Any]):
    @property
    def data(self: Self) -> frozendict[str, Any]:
        "Return the held dictionary data."
        return self._data

    @data.setter
    def data(
        self: Self,
        value: (
            SupportsKeysAndGetitem[object, Any] | Iterable[tuple[object, Any]]
        ),
    ) -> None:
        "Set the held dictionary data from keys and values."
        self._data = frozendict(gendict(value, dump=False))

    def dump(self: Self, stream: Any, /, **kwargs: Any) -> None:
        "Dump the data into a text stream."
        json.dump(dict(gendict(self._data, dump=True)), stream, **kwargs)

    def dumpintofile(self: Self, file: str, /, **kwargs: Any) -> None:
        "Dump the data into a UTF-8 encoded JSON file."
        with open(file, "w", encoding="utf-8") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, **kwargs: Any) -> str:
        "Dump the data as a string."
        return json.dumps(dict(gendict(self._data, dump=True)), **kwargs)

    @classmethod
    def load(cls: type[Self], stream: Any, /, **kwargs: Any) -> Self:
        "Load a JSON object from a text stream."
        value: Any = json.load(stream, **kwargs)
        if not isinstance(value, Mapping):
            raise TypeError("JSONDict can only load a JSON object")
        return cls(value)

    @classmethod
    def loadfromfile(cls: type[Self], file: str, /, **kwargs: Any) -> Self:
        "Load a JSON object from a UTF-8 encoded file."
        with open(file, "r", encoding="utf-8") as stream:
            return cls.load(stream, **kwargs)

    @classmethod
    def loads(cls: type[Self], string: str, /, **kwargs: Any) -> Self:
        "Load a JSON object from a string."
        value: Any = json.loads(string, **kwargs)
        if not isinstance(value, Mapping):
            raise TypeError("JSONDict can only load a JSON object")
        return cls(value)
