"""Test the JSONDict class."""

from __future__ import annotations

__all__: list[str] = ["TestJSONDict"]

import io
import math
import os
import tempfile
import unittest
from datetime import date

from jsonhold import JSONDict, JSONList


class TestJSONDict(unittest.TestCase):
    "Test the JSONDict class and its JSON data handling behavior."

    def test_keys_are_converted_to_strings(self) -> None:
        "Test that keys are converted to strings."
        holder = JSONDict({1: "one", "two": 2})  # type: ignore[arg-type]
        self.assertIn("1", holder.data)
        self.assertNotIn(1, holder.data)
        self.assertEqual(holder.data["1"], "one")
        self.assertEqual(holder.data["two"], 2)

    def test_nested_mappings_and_sequences_are_wrapped(self) -> None:
        "Test that nested mappings and sequences are wrapped in holders."
        holder = JSONDict(
            {
                "object": {"answer": 42},
                "array": ["a", "b", {"nested": True}],
                "string": "abc",
            }
        )
        self.assertIsInstance(holder.data["object"], JSONDict)
        self.assertEqual(holder.data["object"].data["answer"], 42)
        self.assertIsInstance(holder.data["array"], JSONList)
        self.assertEqual(holder.data["array"].data[0], "a")
        self.assertIsInstance(holder.data["array"].data[2], JSONDict)
        self.assertIs(holder.data["array"].data[2].data["nested"], True)
        self.assertEqual(holder.data["string"], "abc")

    def test_supported_scalar_values_are_preserved(self) -> None:
        "Test that JSON scalar values are preserved."
        holder = JSONDict(
            {
                "string": "value",
                "bool": True,
                "int": 123,
                "float": 1.5,
                "none": None,
            }
        )
        self.assertEqual(holder.data["string"], "value")
        self.assertIs(holder.data["bool"], True)
        self.assertEqual(holder.data["int"], 123)
        self.assertEqual(holder.data["float"], 1.5)
        self.assertIsNone(holder.data["none"])

    def test_invalid_value_type_raises_type_error(self) -> None:
        "Test that a non-JSON scalar raises TypeError."
        with self.assertRaises(TypeError):
            JSONDict({"bad": date(2026, 9, 21)})

    def test_nonfinite_float_raises_value_error(self) -> None:
        "Test that non-finite JSON numbers are rejected."
        with self.assertRaises(ValueError):
            JSONDict({"bad": math.inf})

    def test_data_assignment_rebuilds_holder_data(self) -> None:
        "Test that data assignment rebuilds holder data."
        holder = JSONDict({"old": 1})
        holder.data = {"new": [1, 2, 3]}
        self.assertNotIn("old", holder.data)
        self.assertIsInstance(holder.data["new"], JSONList)
        self.assertEqual(holder.data["new"].data, (1, 2, 3))

    def test_dumps_and_loads_round_trip(self) -> None:
        "Test dumps and loads round trip."
        original = JSONDict(
            {
                "project": {"name": "jsonhold", "version": "0.1.0"},
                "numbers": [1, 2, 3],
                "enabled": True,
                "nothing": None,
            }
        )
        dumped = original.dumps(sort_keys=True)
        loaded = JSONDict.loads(dumped)
        self.assertIsInstance(dumped, str)
        self.assertEqual(loaded.data["project"].data["name"], "jsonhold")
        self.assertEqual(loaded.data["numbers"].data, (1, 2, 3))
        self.assertIs(loaded.data["enabled"], True)
        self.assertIsNone(loaded.data["nothing"])

    def test_dump_and_load_text_stream_round_trip(self) -> None:
        "Test dump and load text stream round trip."
        original = JSONDict({"name": "stream", "values": [1, 2]})
        stream = io.StringIO()
        original.dump(stream)
        stream.seek(0)
        loaded = JSONDict.load(stream)
        self.assertEqual(loaded.data["name"], "stream")
        self.assertEqual(loaded.data["values"].data, (1, 2))

    def test_dumpintofile_and_loadfromfile_round_trip(self) -> None:
        "Test dumpintofile and loadfromfile round trip."
        original = JSONDict({"name": "file", "values": [3, 4]})
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.json")
            original.dumpintofile(path, ensure_ascii=False)
            loaded = JSONDict.loadfromfile(path)
        self.assertEqual(loaded.data["name"], "file")
        self.assertEqual(loaded.data["values"].data, (3, 4))

    def test_load_rejects_top_level_array(self) -> None:
        "Test that JSONDict only accepts a JSON object at the top level."
        with self.assertRaises(TypeError):
            JSONDict.loads("[]")


if __name__ == "__main__":
    unittest.main()
