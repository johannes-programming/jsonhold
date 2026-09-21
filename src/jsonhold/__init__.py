"""Export the public JSON data holder classes."""

from __future__ import annotations

__all__: list[str] = ["JSONDict", "JSONList"]

from .core.JSONDict import JSONDict
from .core.JSONList import JSONList
