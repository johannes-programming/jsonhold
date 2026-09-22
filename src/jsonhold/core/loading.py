__all__: list[str] = ["load", "loadfromfile", "loads"]

import io
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from .._utils.funcs import getvalue
from ..core.JSONDict import JSONDict
from ..core.JSONList import JSONList

type JSONValue = JSONDict | JSONList | None | str | int | Decimal


def load(
    stream: io.BufferedReader | io.TextIOWrapper,
    /,
    **kwargs: Any,
) -> JSONValue:
    "Load a JSON object from a text stream."
    return getvalue(json.load(stream, parse_float=Decimal, **kwargs))


def loadfromfile(file: Path | str, /, **kwargs: Any) -> JSONValue:
    "Load a JSON object from a UTF-8 encoded file."
    stream: io.TextIOWrapper
    with open(file, "r") as stream:
        return load(stream, **kwargs)


def loads(
    string: str | bytes | bytearray,
    /,
    **kwargs: Any,
) -> JSONValue:
    "Load a JSON object from a string."
    return getvalue(json.loads(string, parse_float=Decimal, **kwargs))
