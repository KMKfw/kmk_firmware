import busio

import adafruit_displayio_ssd1306  # Display-specific library
import displayio

from . import DisplayBase

# Required to initialize this display
displayio.release_displays()


class SSD1306(DisplayBase):
    def __init__(self, i2c=None, sda=None, scl=None, device_address=0x3C):
        self.device_address = device_address
        # i2c initialization
        self.i2c = i2c
        if self.i2c is None:
            self.i2c = busio.I2C(scl, sda)

    def during_bootup(self, width, height, rotation):
        self.display = adafruit_displayio_ssd1306.SSD1306(
            displayio.I2CDisplay(self.i2c, device_address=self.device_address),
            width=width,
            height=height,
            rotation=rotation,
        )

        return self.display

    def deinit(self):
        self.i2c.deinit()
