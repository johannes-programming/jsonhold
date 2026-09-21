"""Test the JSONList class."""

from __future__ import annotations

__all__: list[str] = ["TestJSONList"]

import io
import os
import tempfile
import unittest

from jsonhold import JSONDict, JSONList


class TestJSONList(unittest.TestCase):
    "Test the JSONList class and its JSON array handling behavior."

    def test_list_data_is_stored_as_tuple(self) -> None:
        "Test that list data is stored as tuple."
        holder = JSONList([1, "two", True, None])
        self.assertEqual(holder.data, (1, "two", True, None))
        self.assertIsInstance(holder.data, tuple)

    def test_nested_values_are_wrapped(self) -> None:
        "Test that nested values are wrapped in holders."
        holder = JSONList([{"name": "item"}, [1, 2], "abc"])
        self.assertIsInstance(holder.data[0], JSONDict)
        self.assertEqual(holder.data[0].data["name"], "item")
        self.assertIsInstance(holder.data[1], JSONList)
        self.assertEqual(holder.data[1].data, (1, 2))
        self.assertEqual(holder.data[2], "abc")

    def test_invalid_list_value_type_raises_type_error(self) -> None:
        "Test that invalid list value type raises TypeError."
        with self.assertRaises(TypeError):
            JSONList([b"bytes"])

    def test_data_assignment_rebuilds_list_data(self) -> None:
        "Test that data assignment rebuilds list data."
        holder = JSONList([1])
        holder.data = [{"nested": "yes"}]
        self.assertEqual(len(holder.data), 1)
        self.assertIsInstance(holder.data[0], JSONDict)
        self.assertEqual(holder.data[0].data["nested"], "yes")

    def test_dumps_and_loads_round_trip(self) -> None:
        "Test a top-level JSON array round trip."
        original = JSONList([1, {"two": 2}, [3, None]])
        dumped = original.dumps()
        loaded = JSONList.loads(dumped)
        self.assertEqual(loaded.data[0], 1)
        self.assertIsInstance(loaded.data[1], JSONDict)
        self.assertEqual(loaded.data[1].data["two"], 2)
        self.assertIsInstance(loaded.data[2], JSONList)
        self.assertEqual(loaded.data[2].data, (3, None))

    def test_dump_and_load_text_stream_round_trip(self) -> None:
        "Test top-level JSON array stream round trip."
        original = JSONList(["stream", {"values": [1, 2]}])
        stream = io.StringIO()
        original.dump(stream)
        stream.seek(0)
        loaded = JSONList.load(stream)
        self.assertEqual(loaded.data[0], "stream")
        self.assertEqual(loaded.data[1].data["values"].data, (1, 2))

    def test_dumpintofile_and_loadfromfile_round_trip(self) -> None:
        "Test top-level JSON array file round trip."
        original = JSONList(["file", 3, 4])
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.json")
            original.dumpintofile(path)
            loaded = JSONList.loadfromfile(path)
        self.assertEqual(loaded.data, ("file", 3, 4))

    def test_load_rejects_top_level_object(self) -> None:
        "Test that JSONList only accepts a JSON array at the top level."
        with self.assertRaises(TypeError):
            JSONList.loads("{}")


if __name__ == "__main__":
    unittest.main()
