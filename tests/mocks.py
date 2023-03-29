import sys
import time
from unittest.mock import Mock


class KeyEvent:
    def __init__(self, key_number, pressed):
        self.key_number = key_number
        self.pressed = pressed


def ticks_ms():
    return (time.time_ns() // 1_000_000) % (1 << 29)


def init_circuit_python_modules_mocks():
    sys.modules['usb_hid'] = Mock()
    sys.modules['digitalio'] = Mock()
    sys.modules['neopixel'] = Mock()
    sys.modules['pulseio'] = Mock()
    sys.modules['busio'] = Mock()
    sys.modules['microcontroller'] = Mock()
    sys.modules['board'] = Mock()
    sys.modules['storage'] = Mock()

    sys.modules['keypad'] = Mock()
    sys.modules['keypad'].Event = KeyEvent

    sys.modules['micropython'] = Mock()
    sys.modules['micropython'].const = lambda x: x

    sys.modules['supervisor'] = Mock()
    sys.modules['supervisor'].ticks_ms = ticks_ms

    from . import task

    sys.modules['_asyncio'] = task
