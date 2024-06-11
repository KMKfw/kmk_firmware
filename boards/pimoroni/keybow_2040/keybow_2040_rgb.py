import board
import busio
from micropython import const

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_pixelbuf import PixelBuf

_SHUTDOWN_REGISTER = const(0x0A)
_CONFIG_BANK = const(0x0B)
_BANK_ADDRESS = const(0xFD)

_ENABLE_OFFSET = const(0x00)
_COLOR_OFFSET = const(0x24)


class Keybow2040Leds(PixelBuf):
    '''Supports the Pimoroni Keybow 2040 with 4x4 matrix of RGB LEDs'''

    width = 16
    height = 3

    # Pixel addresses starting from LED 17,
    # then offset by 1 to fit register addr
    _pixel_addr = [
        (0, 104, 72, 88),  # 0, 0
        (3, 120, 24, 56),  # 1, 0
        (6, 96, 64, 80),  # 2, 0
        (9, 112, 16, 48),  # 3, 0
        (12, 105, 73, 89),  # 0, 1
        (15, 121, 25, 57),  # 1, 1
        (18, 97, 65, 81),  # 2, 1
        (21, 113, 17, 49),  # 3, 1
        (24, 106, 74, 90),  # 0, 2
        (27, 122, 9, 58),  # 1, 2
        (30, 98, 66, 82),  # 2, 2
        (33, 114, 1, 50),  # 3, 2
        (36, 107, 75, 91),  # 0, 3
        (39, 123, 10, 59),  # 1, 3
        (42, 99, 67, 83),  # 2, 3
        (45, 115, 2, 51),  # 3, 3
    ]

    def __init__(self, size: int = 16):  # size kept for backward compatibility
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
        self.i2c_device = I2CDevice(self.i2c, 0x74)
        self.out_buffer = bytearray(124)
        self._pixels = 16
        super().__init__(self._pixels, byteorder='RGB')

        # First byte of buffer is our first LED address
        self.out_buffer[0] = _COLOR_OFFSET + 17

        with self.i2c_device as i2c:
            i2c.write(bytes([_BANK_ADDRESS, 0]))
            i2c.write(bytes([_ENABLE_OFFSET] + [0xFF] * 18))  # Enable all LEDs
            i2c.write(bytes([_COLOR_OFFSET] + [0x00] * 144))  # Init all to 0

            i2c.write(bytes([_BANK_ADDRESS, _CONFIG_BANK]))
            i2c.write(bytes([0x00] * 14))  # Clear Mode, Frame, ... etc
            i2c.write(bytes([_SHUTDOWN_REGISTER, 0x01]))  # 0 == shutdown, 1 == normal

            i2c.write(bytes([_BANK_ADDRESS, 0]))

    def _transmit(self, buffer):
        # Bring buffer into local scope for a tiny perf improvement
        out = self.out_buffer
        # Shuffle the 16 pixel PixelBuf buffer into our 144 LED
        # display native format.
        for o, r, g, b in self._pixel_addr:
            out[r] = buffer[o + 0]
            out[g] = buffer[o + 1]
            out[b] = buffer[o + 2]

        with self.i2c_device as i2c:
            # Write our 124 byte buffer
            # byte 0 is prefilled with the register address
            i2c.write(out)
