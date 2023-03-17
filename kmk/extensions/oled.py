from supervisor import ticks_ms

import adafruit_displayio_ssd1306
import displayio
import terminalio
from adafruit_display_text import label

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key
from kmk.kmktime import check_deadline
from kmk.modules.split import Split, SplitSide
from kmk.utils import clamp


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
        self.x = x
        self.y = y
        if x_anchor == 'L':
            self.x_anchor = 0.0
            self.x = self.x + 1
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
        self.anchored_position = (self.x, self.y)
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
        self.image = image
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
        off_time=60,
        powersave_dim_time=10,
        powersave_off_time=30,
    ):
        self.i2c_bus = i2c
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
        self.off_time_ms = off_time * 1000
        self.powersavedim_time_ms = powersave_dim_time * 1000
        self.powersave_off_time_ms = powersave_off_time * 1000
        self.split_side = None

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

    def render_oled(self, layer):
        splash = displayio.Group()

        for entry in self.entries:
            if entry.layer != layer and entry.layer is not None:
                continue
            if type(entry) is TextEntry:
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
            elif type(entry) is ImageEntry:
                splash.append(
                    displayio.TileGrid(
                        entry.image,
                        pixel_shader=entry.image.pixel_shader,
                        x=entry.x,
                        y=entry.y,
                    )
                )
        self.display.show(splash)

    def updateOLED(self, sandbox):
        self.render_oled(sandbox.active_layers[0])

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, keyboard):

        for module in keyboard.modules:
            if type(module) is Split:
                self.split_side = module.split_side

        if self.split_side == SplitSide.LEFT:
            self.flip = self.flip_left
        if self.split_side == SplitSide.RIGHT:
            self.flip = self.flip_right

        for idx, entry in enumerate(self.entries):
            if entry.side != self.split_side and entry.side is not None:
                del self.entries[idx]

        displayio.release_displays()
        self.display = adafruit_displayio_ssd1306.SSD1306(
            displayio.I2CDisplay(self.i2c_bus, device_address=self.device_address),
            width=self.width,
            height=self.height,
            rotation=180 if self.flip else 0,
            brightness=self.brightness,
        )

    def before_matrix_scan(self, sandbox):
        self.dim()
        if sandbox.active_layers[0] != self.prev_layer:
            self.prev_layer = sandbox.active_layers[0]
            self.updateOLED(sandbox)

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update or keyboard.secondary_matrix_update:
            self.timer_time_reset()

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

    def timer_time_reset(self):
        self.timer_start = ticks_ms()

    def dim(self):
        if self.powersave:

            if self.powersave_off_time_ms != 0 and not check_deadline(
                ticks_ms(), self.timer_start, self.powersave_off_time_ms
            ):
                self.display.sleep()

            elif self.powersave.dim_time_ms != 0 and not check_deadline(
                ticks_ms(), self.timer_start, self.powersave_dim_time_ms
            ):
                self.display.brightness = (
                    self.display.brightness / 2
                    if self.display.brightness > 0.5
                    else 0.1
                )

            else:
                self.display.brightness = self.brightness
                self.display.wake()

        elif self.off_time_ms != 0 and not check_deadline(
            ticks_ms(), self.timer_start, self.off_time_ms
        ):
            self.display.sleep()

        elif self.dim_time_ms != 0 and not check_deadline(
            ticks_ms(), self.timer_start, self.dim_time_ms
        ):
            self.display.brightness = (
                self.display.brightness / 2 if self.display.brightness > 0.5 else 0.1
            )

        else:
            self.display.brightness = self.brightness
            self.display.wake()
