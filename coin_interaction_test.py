"""Coin dragging and payment must not jitter or restack the whole game visibly."""

import ctypes
from dataclasses import replace
import tkinter as tk
from types import SimpleNamespace
from unittest.mock import patch

from doors_ransom import RansomSimulator
from visibility_test import assert_visible, hwnd, pump, user32


