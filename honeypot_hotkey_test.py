"""Deterministic collectible and configurable-command regression tests."""

from dataclasses import replace
from pathlib import Path
import tempfile
import tkinter as tk
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from PIL import Image
from doors_ransom import ASSET_DIR, RansomSimulator, WM_HOTKEY
from hotkey_test import wait_until
from ransom_config import DEFAULT_SETTINGS, RansomSettings, load_settings, save_settings
from ransom_hotkeys import (binding_combinations, capture_binding, command_hotkeys,
                            DEFAULT_COMMAND_HOTKEYS, settings_has_focus, check_available)
from ransom_setting import SettingsWindow


class SettingsPath:
    """A disposable settings path that works with managed Windows temp ACLs."""

    def __enter__(self) -> Path:
        handle = tempfile.NamedTemporaryFile(prefix="ransom-hotkey-", suffix=".json", delete=False)
        self.path = Path(handle.name)
        handle.close()
        self.path.unlink(missing_ok=True)
        return self.path

    def __exit__(self, _type, _value, _traceback) -> None:
        self.path.unlink(missing_ok=True)


class NewSettingsTests(unittest.TestCase):
    def test_validation_and_round_trip(self):
        expected = RansomSettings.from_values(900, 5, 20, .25, "F6", "Ctrl+F7", "Shift+F8", 2.5, 750)
        with SettingsPath() as path:
            save_settings(expected, path)
            self.assertEqual(load_settings(path), expected)
        for changes in ({"honeypot_chance_percent": -1}, {"honeypot_chance_percent": 101},
                        {"honeypot_chance_percent": float("nan")}, {"honeypot_value": 0},
                        {"honeypot_value": 2.5}, {"honeypot_value": True},
                        {"trigger_hotkey": "*"}, {"exit_hotkey": "Shift+Equals"},
                        {"exit_hotkey": "F12"}, {"exit_hotkey": "Alt+F4"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                replace(DEFAULT_SETTINGS, **changes).validated()
        self.assertEqual(command_hotkeys(DEFAULT_SETTINGS), DEFAULT_COMMAND_HOTKEYS)

    def test_local_key_capture(self):
        self.assertEqual(capture_binding(SimpleNamespace(keycode=71, state=5)), "Ctrl+Shift+G")
        self.assertEqual(capture_binding(SimpleNamespace(keycode=117, state=0)), "F6")
        self.assertEqual(capture_binding(SimpleNamespace(keycode=187, state=1)), "Shift+Equals")
        self.assertEqual(capture_binding(SimpleNamespace(keycode=71, state=0x20000)), "Alt+G")
        self.assertEqual(capture_binding(SimpleNamespace(keycode=106, state=0x20000)), "Alt+NumMultiply")
        self.assertIsNone(capture_binding(SimpleNamespace(keycode=16, state=1)))
        self.assertEqual(binding_combinations("Ctrl+Shift+G"), ((6, 71),))
        self.assertEqual(binding_combinations("Alt+NumMultiply"), ((1, 106),))
        self.assertEqual(
            command_hotkeys(replace(DEFAULT_SETTINGS, exit_hotkey="Alt+NumMultiply"))[0x5257],
            ("exit", 0x4001, 106),
        )
