"""Validated settings shared by the encounter and its standalone editor."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
import os
from pathlib import Path
import shlex
import tempfile

from ransom_hotkeys import validate_bindings


@dataclass(frozen=True)
class RansomSettings:
    required_coins: int = 500
    min_spawn_seconds: float = 60.0
    max_spawn_seconds: float = 180.0
    stop_grace_seconds: float = 0.25
    trigger_hotkey: str = "+"
    restore_hotkey: str = "-"
    exit_hotkey: str = "*"
    honeypot_chance_percent: float = 1.0
    honeypot_value: int = 500
    ransom_seconds: float = 90.0
    popup_scale_percent: int = 100
    failure_command: str = ""
