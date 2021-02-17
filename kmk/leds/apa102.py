import digitalio
from micropython import const

from .. import rgb


class RGB(rgb.RGB):
    def setup(self):
        self._sof_length = const(4)
        self._eof_length = const(4)

        self.pin_data = digitalio.DigitalInOut(self.pixel_pin[0])
        self.pin_clock = digitalio.DigitalInOut(self.pixel_pin[1])

        self._buffer = bytearray(
            self.num_pixels * 4 + self._sof_length + self._eof_length
        )

        for x in range(self._sof_length):
            self._buffer[x] = 0b00000000

        for x in range(self._eof_length):
            self._buffer[-x] = 0b11111111

        for x in range(self.num_pixels):
            offset = self._sof_length + (x * 4)
            self._buffer[offset] = 0b11100000 | 31  # TODO: configurable brightness?

    def _to_dict(self):
        # TODO what's `dict(RGB instance)` used for?
        # do we care that it leaks a "neopixel" value enough to overload it?
        return {
            'hue': self.hue,
            'sat': self.sat,
            'val': self.val,
            'time': self.time,
            'intervals': self.intervals,
            'animation_mode': self.animation_mode,
            'animation_speed': self.animation_speed,
            'enabled': self.enabled,
            'disable_auto_write': self.disable_auto_write,
        }

    def _write_byte(self, byte):
        for _ in range(8):
            self.pin_data.write(byte & 0x80)
            self.pin_clock.write(1)
            byte <<= 1
            self.pin_clock.write(0)

    def show(self):
        '''
        Turns on all LEDs without changing stored values
        '''
        for byte in self._buffer:
            self._write_byte(byte)

        return self

    def set_rgb(self, rgb, index):
        '''
        Takes an RGB or RGBW and displays it on a single LED
        :param rgb: RGB or RGBW
        :param index: Index of LED/Pixel
        '''
        if 0 <= index <= self.num_pixels - 1:
            offset = self._sof_length + (index * 4) + 1
            self._buffer[offset : offset + 3] = rgb[:3]

        if not self.disable_auto_write:
            self.show()

        return self

    def set_rgb_fill(self, rgb):
        '''
        Takes an RGB or RGBW and displays it on all LEDs
        :param rgb: RGB or RGBW
        '''
        # TODO optimise to set pixels directly since this will auto-write every pixel
        for index in range(self.num_pixels):
            self.set_rgb(rgb, index)

        if not self.disable_auto_write:
            self.show()

        return self
