import busio

import adafruit_displayio_ssd1306  # Display-specific library
import displayio

from . import DisplayBase

try:
    import i2cdisplaybus

    i2c_display_module = True
except ImportError:
    i2c_display_module = False

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
        if i2c_display_module:
            display_bus = i2cdisplaybus.I2CDisplayBus(
                self.i2c, device_address=self.device_address
            )
        else:
            display_bus = displayio.I2CDisplay(
                self.i2c, device_address=self.device_address
            )
        self.display = adafruit_displayio_ssd1306.SSD1306(
            display_bus,
            width=width,
            height=height,
            rotation=rotation,
        )

        return self.display

    def deinit(self):
        self.i2c.deinit()
