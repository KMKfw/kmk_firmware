import sys
import time
from unittest.mock import Mock


def init_circuit_python_modules_mocks():
    sys.modules['usb_hid'] = Mock()
    sys.modules['digitalio'] = Mock()
    sys.modules['neopixel'] = Mock()
    sys.modules['pulseio'] = Mock()
    sys.modules['busio'] = Mock()
    sys.modules['microcontroller'] = Mock()
    sys.modules['board'] = Mock()
    sys.modules['storage'] = Mock()

    sys.modules['micropython'] = Mock()
    sys.modules['micropython'].const = lambda x: x

    sys.modules['supervisor'] = Mock()
    sys.modules['supervisor'].ticks_ms = lambda: time.time_ns() // 1_000_000
