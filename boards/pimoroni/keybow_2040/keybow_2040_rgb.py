import board
import busio
from micropython import const

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_pixelbuf import PixelBuf

_FRAME_REGISTER = const(0x01)
_SHUTDOWN_REGISTER = const(0x0A)
_CONFIG_BANK = const(0x0B)
_BANK_ADDRESS = const(0xFD)

_ENABLE_OFFSET = const(0x00)
_COLOR_OFFSET = const(0x24)


class Keybow2040Leds(PixelBuf):
    '''Supports the Pimoroni Keybow 2040 with 4x4 matrix of RGB LEDs'''

    width = 16
    height = 3

    def __init__(
            self,
            size: int = 16  # Kept for backward compatibility
    ):
        self.i2c = busio.I2C( board.SCL, board.SDA, frequency=400_000)
        self.i2c_device = I2CDevice(self.i2c, 0x74)
        self.out_buffer = bytearray(144)
        self._pixels = 16
        self._frame = 0
        super().__init__(self._pixels, byteorder='RGB')

        with self.i2c_device as i2c:
            for frame in range(2):
                i2c.write(bytes([_BANK_ADDRESS, frame]))
                i2c.write(bytes([_ENABLE_OFFSET] + [0xFF] * 18))  # Enable all LEDs
                i2c.write(bytes([_COLOR_OFFSET] + [0x00] * 144))  # Init all to 0

            i2c.write(bytes([_BANK_ADDRESS, _CONFIG_BANK]))
            i2c.write(bytes([0x00] * 14))  # Clear Mode, Frame, ... etc
            i2c.write(bytes([_SHUTDOWN_REGISTER, 0x01]))  # 0 == shutdown, 1 == normal

        # Keep track of the LEDs we actually use (48 out of 144)
        # so we can batch up individual i2c transactions and avoid
        # copying unused data.
        self.used_leds = [
            [17, 18],
            [25, 26],
            [32, 33],
            [40, 41],
            [64, 65, 66, 67],
            [72, 73, 74, 75],
            [80, 81, 82, 83],
            [88, 89, 90, 91],
            [96, 97, 98, 99],
            [104, 105, 106, 107],
            [112, 113, 114, 115],
            [120, 121, 122, 123],
            [128, 129, 130, 131],
            [136, 137, 138, 139],
        ]

    def _transmit(self, buffer):
        # Shuffle the 16 pixel PixelBuf buffer into our 144 LED
        # display native format.
        for x in range(self._pixels):
            r, g, b = Keybow2040Leds.pixel_addr(x)
            self.out_buffer[r] = buffer[x * 3 + 0]
            self.out_buffer[g] = buffer[x * 3 + 1]
            self.out_buffer[b] = buffer[x * 3 + 2]

        with self.i2c_device as i2c:
            # Switch to our new (not currently visible) frame
            i2c.write(bytes([_BANK_ADDRESS, self._frame]))

            # Lazy non-batched write, probably fast enough?
            # i2c.write(bytes([_COLOR_OFFSET]) + self.out_buffer)

            # We only actually use 16 * 3 = 48 LEDs out of the 144 total
            # They're kind of awkwardly spread around, but if we batch up
            # the writes it gets the update time from ~0.016ms to ~0.012ms
            for group in self.used_leds:
                offset = group[0]
                count = len(group)
                i2c.write(
                    bytes([_COLOR_OFFSET + offset])
                    + self.out_buffer[offset : offset + count]
                )

            # Set the newly written frame as the visible one
            i2c.write(bytes([_BANK_ADDRESS, _CONFIG_BANK]))
            i2c.write(bytes([_FRAME_REGISTER, self._frame]))

        # Switch to our other buffer
        self._frame = not self._frame

    @staticmethod
    def pixel_addr(x):
        return [
            (120, 88, 104),  # 0, 0
            (136, 40, 72),  # 1, 0
            (112, 80, 96),  # 2, 0
            (128, 32, 64),  # 3, 0
            (121, 89, 105),  # 0, 1
            (137, 41, 73),  # 1, 1
            (113, 81, 97),  # 2, 1
            (129, 33, 65),  # 3, 1
            (122, 90, 106),  # 0, 2
            (138, 25, 74),  # 1, 2
            (114, 82, 98),  # 2, 2
            (130, 17, 66),  # 3, 2
            (123, 91, 107),  # 0, 3
            (139, 26, 75),  # 1, 3
            (115, 83, 99),  # 2, 3
            (131, 18, 67),  # 3, 3
        ][x]
