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

            # We only actually use 16 * 3 = 48 LEDs out of the 144 total
            # but at 400KHz I2C it's cheaper just to write the whole lot
            i2c.write(bytes([_COLOR_OFFSET]) + self.out_buffer)

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
