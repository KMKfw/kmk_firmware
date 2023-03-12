import busio
from supervisor import ticks_ms

import adafruit_displayio_ssd1306
import displayio
import terminalio
from adafruit_display_text import label

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key
from kmk.kmktime import check_deadline
from kmk.utils import clamp


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
        x_anchor='left',
        y_anchor='top',
        direction='LTR',
        line_spacing=0.75,
        inverted=False,
        layer=None,
        side=None,
    ):
        _x = 0
        _x_anchor = 0.0
        _y_anchor = 0.0
        if x_anchor == 'L':
            _x_anchor = 0.0
        elif x_anchor == 'M':
            _x_anchor = 0.5
        elif x_anchor == 'R':
            _x_anchor = 1.0
        else:
            _x_anchor = 0.0
        if y_anchor == 'T':
            _y_anchor = 0.0
        elif y_anchor == 'M':
            _y_anchor = 0.5
        elif y_anchor == 'B':
            _y_anchor = 1.0
        else:
            _y_anchor = 0.0
        if x_anchor != 'm' or x_anchor != 'r':
            _x = x + 1
        else:
            _x = x
        return {
            0: text,
            1: _x,
            2: y,
            3: side,
            4: layer,
            5: OledEntryType.TXT,
            6: _x_anchor,
            7: _y_anchor,
            8: direction,
            9: line_spacing,
            10: inverted,
        }

    @staticmethod
    def oled_image_entry(x=0, y=0, image='', layer=None, side=None):
        odb = displayio.OnDiskBitmap(image)
        return {
            0: odb,
            1: x,
            2: y,
            3: side,
            4: layer,
            5: OledEntryType.IMG,
        }


class Oled(Extension):
    def __init__(
        self,
        views,
        width=128,
        height=32,
        split=None,
        flip: bool = False,
        flip_left: bool = False,
        flip_right: bool = False,
        device_address=0x3C,
        brightness=0.8,
        brightness_step=0.1,
        dim_time=None,
        off_time=None,
        powersave_dim_time=10,
        powersave_off_time=60,
    ):
        self._flip = flip
        self._flip_left = flip_left
        self._flip_right = flip_right
        self._views = views.data
        self._width = width
        self._height = height
        self._prevLayers = 0
        self._device_address = device_address
        self._brightness = brightness
        self._brightness_step = brightness_step
        self._timer_start = ticks_ms()
        self._powersave = False
        self._dim_time_ms = dim_time * 1000 if dim_time else None
        self._off_time_ms = off_time * 1000 if off_time else None
        self._powersave_dim_time_ms = (
            powersave_dim_time * 1000 if powersave_dim_time else None
        )
        self._powersave_off_time_ms = (
            powersave_off_time * 1000 if powersave_off_time else None
        )
        self._split = split

        make_key(
            names=('OLED_BRI',),
            on_press=self._oled_brightness_increase,
            on_release=handler_passthrough,
        )
        make_key(
            names=('OLED_BRD',),
            on_press=self._oled_brightness_decrease,
            on_release=handler_passthrough,
        )

    def render_oled(self, layer):
        splash = displayio.Group()

        for view in self._views:
            if view[4] == layer or view[4] is None:
                if view[5] == OledEntryType.TXT:
                    splash.append(
                        label.Label(
                            terminalio.FONT,
                            text=view[0],
                            color=0xFFFFFF if not view[10] else 0x000000,
                            background_color=0x000000 if not view[10] else 0xFFFFFF,
                            anchor_point=(view[6], view[7]),
                            anchored_position=(view[1], view[2]),
                            label_direction=view[8],
                            line_spacing=view[9],
                            padding_left=1,
                        )
                    )
                elif view[5] == OledEntryType.IMG:
                    splash.append(
                        displayio.TileGrid(
                            view[0],
                            pixel_shader=view[0].pixel_shader,
                            x=view[1],
                            y=view[2],
                        )
                    )
        self._display.show(splash)

    def updateOLED(self, sandbox):
        self.render_oled(sandbox.active_layers[0])

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, keyboard):
        if self._split is not None:
            if self._split.split_side == 1:
                self.split_side = 'L'
                self._flip = self._flip_left
            elif self._split.split_side == 2:
                self.split_side = 'R'
                self._flip = self._flip_right
        else:
            self.split_side = None

        for idx, view in enumerate(self._views):
            if view[3] != self.split_side and view[3] is not None:
                del self._views[idx]

        displayio.release_displays()
        i2c = busio.I2C(keyboard.SCL, keyboard.SDA)
        self._display = adafruit_displayio_ssd1306.SSD1306(
            displayio.I2CDisplay(i2c, device_address=self._device_address),
            width=self._width,
            height=self._height,
            rotation=180 if self._flip else 0,
            brightness=self._brightness,
        )
        self.render_oled(0)

    def before_matrix_scan(self, sandbox):
        self.dim()
        if sandbox.active_layers[0] != self._prevLayers:
            self._prevLayers = sandbox.active_layers[0]
            self.updateOLED(sandbox)

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update or keyboard.secondary_matrix_update:
            self.timer_time_reset()

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        self._powersave = True

    def on_powersave_disable(self, sandbox):
        self._powersave = False

    def _oled_brightness_increase(self):
        self._display.brightness = clamp(
            self._display.brightness + self._brightness_step, 0, 1
        )
        self._brightness = self._display.brightness  # Save current brightness

    def _oled_brightness_decrease(self):
        self._display.brightness = clamp(
            self._display.brightness - self._brightness_step, 0, 1
        )
        self._brightness = self._display.brightness  # Save current brightness

    def timer_time_reset(self):
        self._timer_start = ticks_ms()

    def dim(self):
        if self._powersave:

            if self._powersave_off_time_ms is not None and not check_deadline(
                ticks_ms(), self._timer_start, self._powersave_off_time_ms
            ):
                self._display.sleep()

            elif self._powersave_dim_time_ms is not None and not check_deadline(
                ticks_ms(), self._timer_start, self._powersave_dim_time_ms
            ):
                self._display.brightness = (
                    self._display.brightness / 2
                    if self._display.brightness > 0.5
                    else 0.1
                )

            else:
                self._display.brightness = self._brightness
            self._display.wake()

        elif self._off_time_ms is not None and not check_deadline(
            ticks_ms(), self._timer_start, self._off_time_ms
        ):
            self._display.sleep()

        elif self._dim_time_ms is not None and not check_deadline(
            ticks_ms(), self._timer_start, self._dim_time_ms
        ):
            self._display.brightness = (
                self._display.brightness / 2 if self._display.brightness > 0.5 else 0.1
            )

        else:
            self._display.brightness = self._brightness
            self._display.wake()
