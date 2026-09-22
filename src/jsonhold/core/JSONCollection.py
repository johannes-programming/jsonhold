"""Provide the JSONCollection class for holding JSON object data."""

from __future__ import annotations

__all__: list[str] = ["JSONCollection"]

import io
import json
from abc import abstractmethod
from collections import abc
from pathlib import Path
from typing import Any, Self


class JSONCollection[Value](abc.Collection[Value]):

    __slots__ = ()

    @abstractmethod
    def _dump(self: Self, /) -> dict[str, Any] | list[Any]: ...

    def dump(
        self: Self,
        stream: io.BufferedWriter | io.TextIOWrapper,
        /,
        **kwargs: Any,
    ) -> None:
        "Dump the data into a text stream."
        json.dump(
            self._dump(),
            stream,  # type: ignore[arg-type]
            **kwargs,
        )

    def dumpintofile(
        self: Self,
        file: Path | str,
        /,
        **kwargs: Any,
    ) -> None:
        "Dump the data into a JSON file."
        stream: io.TextIOWrapper
        with open(file, "w") as stream:
            self.dump(stream, **kwargs)

    def dumps(self: Self, /, **kwargs: Any) -> str:
        "Dump the data as a string."
        return json.dumps(self._dump(), **kwargs)
