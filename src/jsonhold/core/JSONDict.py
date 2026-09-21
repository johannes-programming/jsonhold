"""Provide the JSONDict class for holding JSON object data."""

from __future__ import annotations

__all__: list[str] = ["JSONDict"]

import io
import json
from collections import abc
from typing import Any, Self

import datahold
from frozendict import frozendict

from .._utils.funcs import SupportsKeysAndGetitem, gendict


class JSONDict(datahold.HoldDict[str, Any]):

    __slots__ = ()

    @property
    def data(self: Self) -> frozendict[str, Any]:
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

    def dump(
        self: Self,
        stream: io.BufferedWriter,
        /,
        **kwargs: Any,
    ) -> None:
        "Dump the data into a text stream."
        json.dump(dict(gendict(self._data, dump=True)), stream, **kwargs)

    def dumpintofile(self: Self, file: str, /, **kwargs: Any) -> None:
        "Dump the data into a UTF-8 encoded JSON file."
        with open(file, "w", encoding="utf-8") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, **kwargs: Any) -> str:
        "Dump the data as a string."
        return json.dumps(dict(gendict(self._data, dump=True)), **kwargs)
