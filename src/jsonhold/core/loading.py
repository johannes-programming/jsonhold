__all__: list[str] = ["load", "loadfromfile", "loads"]

import io
import json
from decimal import Decimal
from typing import Any

from .._utils.funcs import getvalue
from ..core.JSONDict import JSONDict
from ..core.JSONList import JSONList

type JSONValue = JSONDict | JSONList | None | str | int | Decimal


def load(
    stream: io.BufferedReader,
    /,
    **kwargs: Any,
) -> JSONValue:
    "Load a JSON object from a text stream."
    return getvalue(json.load(stream, **kwargs))


def loadfromfile(file: str, /, **kwargs: Any) -> JSONValue:
    "Load a JSON object from a UTF-8 encoded file."
    with open(file, "rb") as stream:
        return load(stream, **kwargs)


def loads(
    string: str,
    /,
    **kwargs: Any,
) -> JSONValue:
    "Load a JSON object from a string."
    return getvalue(json.loads(string, **kwargs))
