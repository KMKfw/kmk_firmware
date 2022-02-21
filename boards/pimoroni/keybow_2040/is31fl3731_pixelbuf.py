'''
Simple PixelBuf wrapper for the IS31FL3731 controller used for the Keybow2040's RGB LEDs.
'''

import board

from adafruit_is31fl3731.keybow2040 import Keybow2040 as KeybowLeds
from adafruit_pixelbuf import PixelBuf


class Keybow2040Leds(PixelBuf):
    '''
    Minimal PixelBuf wrapper for the Keybow 2040's LED array.
    '''

    def __init__(self, size: int):
        self.leds = KeybowLeds(board.I2C())
        self._pixels = size
        super().__init__(size, byteorder='RGB')

    def _transmit(self, buffer):
        for pixel in range(self._pixels):
            r = buffer[pixel * 3 + 0]
            g = buffer[pixel * 3 + 1]
            b = buffer[pixel * 3 + 2]
            self.leds.pixelrgb(pixel // 4, pixel % 4, r, g, b)
