import sys
import time
from unittest.mock import MagicMock, Mock


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
    sys.modules['board'] = MagicMock()
    sys.modules['storage'] = Mock()

    sys.modules['keypad'] = Mock()
    sys.modules['keypad'].Event = KeyEvent

    sys.modules['micropython'] = Mock()
    sys.modules['micropython'].const = lambda x: x

    sys.modules['supervisor'] = Mock()
    sys.modules['supervisor'].ticks_ms = ticks_ms
    sys.modules['usb_cdc'] = Mock()

    from . import task

    sys.modules['_asyncio'] = task


def init_board_module_mocks():
    init_circuit_python_modules_mocks()
    sys.modules['rp2pio'] = Mock()
    sys.modules['pwmio'] = Mock()
    sys.modules['rotaryio'] = Mock()
    sys.modules['displayio'] = Mock()
    sys.modules['terminalio'] = Mock()
    sys.modules['adafruit_pixelbuf'] = Mock()
    sys.modules['adafruit_pixelbuf'].PixelBuf = Mock()
    sys.modules['adafruit_displayio_ssd1306'] = Mock()
    sys.modules['adafruit_display_text'] = Mock()
