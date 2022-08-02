import busio
import gc

from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key
import adafruit_displayio_ssd1306
import displayio
import terminalio
from adafruit_display_text import label

from kmk.extensions import Extension

DISPLAY_OFFSET = 10


class OledData:
    def __init__(
        self,
        labels=None,
    ):
        if labels != None:
            self.data = labels


class Oled(Extension):
    def __init__(
        self,
        views,
        oWidth=128,
        oHeight=32,
        flip: bool = False,
        device_address=0x3C,
        brightness=0.8,
    ):
        displayio.release_displays()
        self.rotation = 180 if flip else 0
        self._views = views.data
        self._width = oWidth
        self._height = oHeight
        self._prevLayers = 0
        self._device_address = device_address
        self._brightness = brightness
        gc.collect()

        make_key(
            names=('OLED_BRI',), on_press=self._oled_bri, on_release=handler_passthrough
        )
        make_key(
            names=('OLED_BRD',), on_press=self._oled_brd, on_release=handler_passthrough
        )

    @staticmethod
    def oled_text_entry(x=0, y=0, text="", layer=None):
        return {
            0: label.Label(
                terminalio.FONT,
                text=text,
                color=0xFFFFFF,
                x=x,
                y=y + DISPLAY_OFFSET,
            ),
            1: layer,
        }

    @staticmethod
    def oled_image_entry(x=0, y=0, image="", layer=None):
        odb = displayio.OnDiskBitmap(image)
        return {
            0: displayio.TileGrid(
                odb, pixel_shader=odb.pixel_shader, x=x, y=y + DISPLAY_OFFSET
            ),
            1: layer,
        }

    def render_oled(self, layer):
        splash = displayio.Group()
        self._display.show(splash)
        print(f"views={self._views}, layer={layer}")
        for view in self._views:
            if view[1] == layer or view[1] == None:
                splash.append(view[0])
        gc.collect()

    def updateOLED(self, sandbox):
        self.render_oled(sandbox.active_layers[0])
        gc.collect()

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, board):
        displayio.release_displays()
        i2c = busio.I2C(board.SCL, board.SDA)
        self._display = adafruit_displayio_ssd1306.SSD1306(
            displayio.I2CDisplay(i2c, device_address=self._device_address),
            width=self._width,
            height=self._height,
            rotation=self.rotation,
            brightness=self._brightness,
        )
        self.render_oled(0)
        return

    def before_matrix_scan(self, sandbox):
        if sandbox.active_layers[0] != self._prevLayers:
            self._prevLayers = sandbox.active_layers[0]
            self.updateOLED(sandbox)
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return

    def _oled_bri(self, *args, **kwargs):
        self._display.brightness = (
            self._display.brightness + 0.1 if self._display.brightness < 0.9 else 1.0
        )

    def _oled_brd(self, *args, **kwargs):
        self._display.brightness = (
            self._display.brightness - 0.1 if self._display.brightness > 0.1 else 0.1
        )
