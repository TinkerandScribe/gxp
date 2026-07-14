"""Hidden tests for 07-deep-merge."""

import importlib.util
import os
import unittest
from pathlib import Path


def load_fn():
    p = os.environ.get("IMPL_PATH")
    path = Path(p) if p else Path(__file__).resolve().parent / "deep_merge.py"
    spec = importlib.util.spec_from_file_location("under_test", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.deep_merge


class TestDeepMerge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._fn = load_fn()

    def dm(self, *a, **k):
        return type(self)._fn(*a, **k)

    def test_simple_override(self):
        self.assertEqual(self.dm({"a": 1}, {"a": 2, "b": 3}), {"a": 2, "b": 3})

    def test_nested_merge(self):
        base = {"a": {"x": 1, "y": 2}, "k": 0}
        over = {"a": {"y": 9, "z": 3}}
        self.assertEqual(self.dm(base, over), {"a": {"x": 1, "y": 9, "z": 3}, "k": 0})

    def test_no_mutate_inputs(self):
        base = {"a": {"x": 1}, "L": [1, 2]}
        over = {"a": {"y": 2}, "L": [3]}
        base_snap = {"a": {"x": 1}, "L": [1, 2]}
        over_snap = {"a": {"y": 2}, "L": [3]}
        out = self.dm(base, over, list_mode="extend")
        self.assertEqual(base, base_snap)
        self.assertEqual(over, over_snap)
        out["a"]["x"] = 99
        out["L"].append(7)
        self.assertEqual(base["a"]["x"], 1)
        self.assertEqual(base["L"], [1, 2])

    def test_none_deletes_key(self):
        self.assertEqual(self.dm({"a": 1, "b": 2}, {"b": None}), {"a": 1})

    def test_none_delete_nested_via_parent_replace(self):
        # None only deletes when that key's override value is None
        self.assertEqual(
            self.dm({"a": {"x": 1, "y": 2}}, {"a": {"y": None}}),
            {"a": {"x": 1}},
        )

    def test_list_replace(self):
        self.assertEqual(
            self.dm({"L": [1, 2]}, {"L": [9]}, list_mode="replace"),
            {"L": [9]},
        )

    def test_list_extend(self):
        self.assertEqual(
            self.dm({"L": [1, 2]}, {"L": [2, 3]}, list_mode="extend"),
            {"L": [1, 2, 2, 3]},
        )

    def test_list_unique(self):
        self.assertEqual(
            self.dm({"L": [1, 2]}, {"L": [2, 3]}, list_mode="unique"),
            {"L": [1, 2, 3]},
        )

    def test_dict_over_list_wins(self):
        self.assertEqual(self.dm({"a": [1]}, {"a": {"x": 1}}), {"a": {"x": 1}})

    def test_list_over_dict_wins(self):
        self.assertEqual(self.dm({"a": {"x": 1}}, {"a": [1, 2]}), {"a": [1, 2]})

    def test_unknown_list_mode(self):
        with self.assertRaises(ValueError) as ctx:
            self.dm({"L": [1]}, {"L": [2]}, list_mode="zip")
        self.assertIn("list_mode", str(ctx.exception).lower())

    def test_unknown_list_mode_without_lists(self):
        with self.assertRaises(ValueError) as ctx:
            self.dm({"a": 1}, {"b": 2}, list_mode="zip")
        self.assertIn("list_mode", str(ctx.exception).lower())

    def test_deep_copy_nested_list_in_dict(self):
        base = {"a": {"L": [1, {"z": 1}]}}
        over = {"b": 1}
        out = self.dm(base, over)
        out["a"]["L"][1]["z"] = 9
        self.assertEqual(base["a"]["L"][1]["z"], 1)

    def test_result_list_not_shared_with_override(self):
        over = {"L": [1, 2]}
        out = self.dm({}, over, list_mode="replace")
        out["L"].append(3)
        self.assertEqual(over["L"], [1, 2])

    def test_only_override_key(self):
        self.assertEqual(self.dm({}, {"a": {"x": [1]}}), {"a": {"x": [1]}})

    def test_base_only_key_kept(self):
        self.assertEqual(self.dm({"keep": 1}, {"add": 2}), {"keep": 1, "add": 2})
