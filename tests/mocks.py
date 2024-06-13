import sys
import time
from unittest.mock import Mock


class KeyEvent:
    def __init__(self, key_number, pressed):
        self.key_number = key_number
        self.pressed = pressed


def ticks_ms():
    return (time.time_ns() // 1_000_000) % (1 << 29)


class Device:
    def __init__(self, usage_page, usage):
        self.usage_page = usage_page
        self.usage = usage
        self.reports = []

    def send_report(self, report):
        self.reports.append(report[:])


def init_circuit_python_modules_mocks():
    sys.modules['usb_hid'] = Mock()
    sys.modules['mock_hid'] = Mock()
    sys.modules['mock_hid'].devices = [
        Device(p, u)
        for p, u in [
            (0x01, 0x06),  # keyboard
            (0x01, 0x02),  # mouse
            (0x0C, 0x01),  # consumer control
        ]
    ]

    sys.modules['digitalio'] = Mock()
    sys.modules['neopixel'] = Mock()
    sys.modules['pulseio'] = Mock()
    sys.modules['busio'] = Mock()
    sys.modules['microcontroller'] = Mock()
    sys.modules['board'] = Mock()
    sys.modules['storage'] = Mock()

    sys.modules['gc'] = Mock()
    sys.modules['gc'].mem_alloc = lambda: 0
    sys.modules['gc'].mem_free = lambda: 0

    sys.modules['keypad'] = Mock()
    sys.modules['keypad'].Event = KeyEvent

    sys.modules['micropython'] = Mock()
    sys.modules['micropython'].const = lambda x: x

    sys.modules['supervisor'] = Mock()
    sys.modules['supervisor'].ticks_ms = ticks_ms
    sys.modules['usb_cdc'] = Mock()

    from . import task

    sys.modules['_asyncio'] = task
