# call this script like:
#   python -m tests.mock_board boards/nullbitsco/tidbit

import sys
from unittest.mock import Mock

from .mocks import init_circuit_python_modules_mocks

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

sys.path.insert(0, sys.argv[1])

# TODO pass tests for dactyl keebs which seem to map a mystery pin B7
if 'dactyl' in sys.argv[1]:
    from kmk.quickpin.pro_micro.avr_promicro import translate as avr

    avr['B7'] = -1

if __name__ == '__main__':
    import main

    assert main
