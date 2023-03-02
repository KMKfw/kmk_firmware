import busio
import gc
from supervisor import ticks_ms

import adafruit_displayio_ssd1306
import displayio
import terminalio
from adafruit_display_text import label

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key
from kmk.kmktime import check_deadline


class OledEntryType:
    TXT = 0
    IMG = 1


class OledData:
    def __init__(
        self,
        entries=None,
    ):
        if entries is not None:
            self.data = entries

    @staticmethod
    def oled_text_entry(
        text='',
        x=0,
        y=0,
        x_anchor=0.0,
        y_anchor=0.0,
        direction='LTR',
        line_spacing=0.75,
        inverted=False,
        layer=None,
    ):
        return {
            0: text,
            1: x,
            2: y,
            3: layer,
            4: OledEntryType.TXT,
            5: x_anchor,
            6: y_anchor,
            7: direction,
            8: line_spacing,
            9: inverted,
        }

    @staticmethod
    def oled_image_entry(x=0, y=0, image='', layer=None):
        odb = displayio.OnDiskBitmap(image)
        return {
            0: odb,
            1: x,
            2: y,
            3: layer,
            4: OledEntryType.IMG,
        }


class Oled(Extension):
    def __init__(
        self,
        views,
        width=128,
        height=32,
        flip: bool = False,
        device_address=0x3C,
        brightness=0.8,
        brightness_step=0.1,
        dim_time=3,
        off_time=6,
    ):
        displayio.release_displays()
        self.rotation = 180 if flip else 0
        self._views = views.data
        self._width = width
        self._height = height
        self._prevLayers = 0
        self._device_address = device_address
        self._brightness = brightness
        self._brightness_step = brightness_step
        self._timer_start = ticks_ms()
        self._dark = False
        self._go_dark = False
        self._dim_time_ms = dim_time * 1000
        self._off_time_ms = off_time * 1000
        gc.collect()

        make_key(
            names=('OLED_BRI',), on_press=self._oled_bri, on_release=handler_passthrough
        )
        make_key(
            names=('OLED_BRD',), on_press=self._oled_brd, on_release=handler_passthrough
        )

    def render_oled(self, layer, *args, **kwargs):
        splash = displayio.Group()

        for view in self._views:
            if self._dark is False:
                if view[3] == layer or view[3] is None:
                    if view[4] == OledEntryType.TXT:
                        splash.append(
                            label.Label(
                                terminalio.FONT,
                                text=view[0],
                                color=0xFFFFFF if not view[9] else 0x000000,
                                background_color=0x000000 if not view[9] else 0xFFFFFF,
                                anchor_point=(view[5], view[6]),
                                anchored_position=(
                                    view[1] if not view[9] else view[1] + 1,
                                    view[2],
                                ),
                                label_direction=view[7],
                                line_spacing=view[8],
                                padding_left=1,
                            )
                        )
                    elif view[4] == OledEntryType.IMG:
                        splash.append(
                            displayio.TileGrid(
                                view[0],
                                pixel_shader=view[0].pixel_shader,
                                x=view[1],
                                y=view[2],
                            )
                        )
        gc.collect()
        self._display.show(splash)

    def updateOLED(self, sandbox):
        self.render_oled(sandbox.active_layers[0])
        gc.collect()

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, keyboard):
        displayio.release_displays()
        i2c = busio.I2C(keyboard.SCL, keyboard.SDA)
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
        self.dim()
        if self._dark != self._go_dark or sandbox.active_layers[0] != self._prevLayers:
            self._dark = self._go_dark
            self._prevLayers = sandbox.active_layers[0]
            self.updateOLED(sandbox)
        return

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update or keyboard.secondary_matrix_update:
            self.timer_time_reset()
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        self._display.brightness = (
            self._display.brightness / 2 if self._display.brightness > 0.5 else 0.2
        )
        return

    def on_powersave_disable(self, sandbox):
        self._display.brightness = (
            self._brightness
        )  # Restore brightness to default or previous value
        return

    def _oled_bri(self, *args, **kwargs):
        self._display.brightness = (
            self._display.brightness + self._brightness_step
            if self._display.brightness + self._brightness_step <= 1.0
            else 1.0
        )
        self._brightness = self._display.brightness  # Save current brightness

    def _oled_brd(self, *args, **kwargs):
        self._display.brightness = (
            self._display.brightness - self._brightness_step
            if self._display.brightness - self._brightness_step >= 0.1
            else 0.1
        )
        self._brightness = self._display.brightness  # Save current brightness

    def timer_time_reset(self):
        self._timer_start = ticks_ms()

    def dim(self):
        if not check_deadline(ticks_ms(), self._timer_start, self._off_time_ms):
            self._go_dark = True
        elif not check_deadline(ticks_ms(), self._timer_start, self._dim_time_ms):
            if self._display.brightness > 0.2:
                self._display.brightness = 0.2
        else:
            self._display.brightness = self._brightness
            self._go_dark = False
