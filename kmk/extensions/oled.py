import busio
from supervisor import ticks_ms

import adafruit_displayio_ssd1306
import displayio
import terminalio
from adafruit_display_text import label

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key
from kmk.kmktime import PeriodicTimer, ticks_diff
from kmk.modules.split import Split, SplitSide
from kmk.utils import clamp

displayio.release_displays()


class TextEntry:
    def __init__(
        self,
        text='',
        x=0,
        y=0,
        x_anchor='L',
        y_anchor='T',
        direction='LTR',
        line_spacing=0.75,
        inverted=False,
        layer=None,
        side=None,
    ):
        self.text = text
        self.direction = direction
        self.line_spacing = line_spacing
        self.inverted = inverted
        self.layer = layer
        self.color = 0xFFFFFF
        self.background_color = 0x000000
        self.x_anchor = 0.0
        self.y_anchor = 0.0
        if x_anchor == 'L':
            self.x_anchor = 0.0
            x = x + 1
        if x_anchor == 'M':
            self.x_anchor = 0.5
        if x_anchor == 'R':
            self.x_anchor = 1.0
        if y_anchor == 'T':
            self.y_anchor = 0.0
        if y_anchor == 'M':
            self.y_anchor = 0.5
        if y_anchor == 'B':
            self.y_anchor = 1.0
        self.anchor_point = (self.x_anchor, self.y_anchor)
        self.anchored_position = (x, y)
        if inverted:
            self.color = 0x000000
            self.background_color = 0xFFFFFF
        self.side = side
        if side == 'L':
            self.side = SplitSide.LEFT
        if side == 'R':
            self.side = SplitSide.RIGHT


class ImageEntry:
    def __init__(self, x=0, y=0, image='', layer=None, side=None):
        self.x = x
        self.y = y
        self.image = displayio.OnDiskBitmap(image)
        self.layer = layer
        self.side = side
        if side == 'L':
            self.side = SplitSide.LEFT
        if side == 'R':
            self.side = SplitSide.RIGHT


class Oled(Extension):
    def __init__(
        self,
        i2c=None,
        sda=None,
        scl=None,
        device_address=0x3C,
        entries=[],
        width=128,
        height=32,
        flip: bool = False,
        flip_left: bool = False,
        flip_right: bool = False,
        brightness=0.8,
        brightness_step=0.1,
        dim_time=20,
        dim_target=0.1,
        off_time=60,
        powersave_dim_time=10,
        powersave_dim_target=0.1,
        powersave_off_time=30,
    ):
        self.device_address = device_address
        self.flip = flip
        self.flip_left = flip_left
        self.flip_right = flip_right
        self.entries = entries
        self.width = width
        self.height = height
        self.prev_layer = None
        self.brightness = brightness
        self.brightness_step = brightness_step
        self.timer_start = ticks_ms()
        self.powersave = False
        self.dim_time_ms = dim_time * 1000
        self.dim_target = dim_target
        self.off_time_ms = off_time * 1000
        self.powersavedim_time_ms = powersave_dim_time * 1000
        self.powersave_dim_target = powersave_dim_target
        self.powersave_off_time_ms = powersave_off_time * 1000
        self.dim_period = PeriodicTimer(50)
        self.split_side = None
        # i2c initialization
        self.i2c = i2c
        if self.i2c is None:
            self.i2c = busio.I2C(scl, sda)

        make_key(
            names=('OLED_BRI',),
            on_press=self.oled_brightness_increase,
            on_release=handler_passthrough,
        )
        make_key(
            names=('OLED_BRD',),
            on_press=self.oled_brightness_decrease,
            on_release=handler_passthrough,
        )

    def render(self, layer):
        splash = displayio.Group()

        for entry in self.entries:
            if entry.layer != layer and entry.layer is not None:
                continue
            if isinstance(entry, TextEntry):
                splash.append(
                    label.Label(
                        terminalio.FONT,
                        text=entry.text,
                        color=entry.color,
                        background_color=entry.background_color,
                        anchor_point=entry.anchor_point,
                        anchored_position=entry.anchored_position,
                        label_direction=entry.direction,
                        line_spacing=entry.line_spacing,
                        padding_left=1,
                    )
                )
            elif isinstance(entry, ImageEntry):
                splash.append(
                    displayio.TileGrid(
                        entry.image,
                        pixel_shader=entry.image.pixel_shader,
                        x=entry.x,
                        y=entry.y,
                    )
                )
        self.display.show(splash)

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, keyboard):

        for module in keyboard.modules:
            if isinstance(module, Split):
                self.split_side = module.split_side

        if self.split_side == SplitSide.LEFT:
            self.flip = self.flip_left
        elif self.split_side == SplitSide.RIGHT:
            self.flip = self.flip_right

        for idx, entry in enumerate(self.entries):
            if entry.side != self.split_side and entry.side is not None:
                del self.entries[idx]

        self.display = adafruit_displayio_ssd1306.SSD1306(
            displayio.I2CDisplay(self.i2c, device_address=self.device_address),
            width=self.width,
            height=self.height,
            rotation=180 if self.flip else 0,
            brightness=self.brightness,
        )

    def before_matrix_scan(self, sandbox):
        if self.dim_period.tick():
            self.dim()
        if sandbox.active_layers[0] != self.prev_layer:
            self.prev_layer = sandbox.active_layers[0]
            self.render(sandbox.active_layers[0])

    def after_matrix_scan(self, sandbox):
        if sandbox.matrix_update or sandbox.secondary_matrix_update:
            self.timer_start = ticks_ms()

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        self.powersave = True

    def on_powersave_disable(self, sandbox):
        self.powersave = False

    def deinit(self, sandbox):
        displayio.release_displays()
        self.i2c.deinit()

    def oled_brightness_increase(self):
        self.display.brightness = clamp(
            self.display.brightness + self.brightness_step, 0, 1
        )
        self.brightness = self.display.brightness  # Save current brightness

    def oled_brightness_decrease(self):
        self.display.brightness = clamp(
            self.display.brightness - self.brightness_step, 0, 1
        )
        self.brightness = self.display.brightness  # Save current brightness

    def dim(self):
        if self.powersave:

            if (
                self.powersave_off_time_ms
                and ticks_diff(ticks_ms(), self.timer_start)
                > self.powersave_off_time_ms
            ):
                self.display.sleep()

            elif (
                self.powersave_dim_time_ms
                and ticks_diff(ticks_ms(), self.timer_start)
                > self.powersave_dim_time_ms
            ):
                self.display.brightness = self.powersave_dim_target

            else:
                self.display.brightness = self.brightness
                self.display.wake()

        elif (
            self.off_time_ms
            and ticks_diff(ticks_ms(), self.timer_start) > self.off_time_ms
        ):
            self.display.sleep()

        elif (
            self.dim_time_ms
            and ticks_diff(ticks_ms(), self.timer_start) > self.dim_time_ms
        ):
            self.display.brightness = self.dim_target

        else:
            self.display.brightness = self.brightness
            self.display.wake()
