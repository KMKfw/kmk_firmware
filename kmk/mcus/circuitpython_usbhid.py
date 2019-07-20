from kmk.hid import CircuitPythonUSB_HID
from kmk.keyboard_config import KeyboardConfig as _KeyboardConfig


class KeyboardConfig(_KeyboardConfig):
    hid_helper = CircuitPythonUSB_HID
