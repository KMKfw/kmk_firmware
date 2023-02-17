import neopixel

from storage import getmount

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key


class Color:
    OFF = [0, 0, 0]
    BLACK = OFF
    WHITE = [249, 249, 249]
    RED = [255, 0, 0]
    AZURE = [153, 245, 255]
    BLUE = [0, 0, 255]
    CYAN = [0, 255, 255]
    GREEN = [0, 255, 0]
    YELLOW = [255, 247, 0]
    MAGENTA = [255, 0, 255]
    ORANGE = [255, 77, 0]
    PURPLE = [255, 0, 242]
    TEAL = [0, 128, 128]
    PINK = [255, 0, 255]


class Rgb_matrix_data:
    def __init__(self, keys=[], underglow=[]):
        if len(keys) == 0:
            print('No colors passed for your keys')
            return
        if len(underglow) == 0:
            print('No colors passed for your underglow')
            return
        self.data = keys + underglow

    @staticmethod
    def generate_led_map(
        number_of_keys, number_of_underglow, key_color, underglow_color
    ):
        keys = [key_color] * number_of_keys
        underglow = [underglow_color] * number_of_underglow
        print(f'Rgb_matrix_data(keys={keys},\nunderglow={underglow})')


class Rgb_matrix(Extension):
    def __init__(
        self,
        rgb_order=(1, 0, 2),  # GRB WS2812
        disable_auto_write=False,
        ledDisplay=[],
        split=False,
        rightSide=False,
    ):
        name = str(getmount('/').label)
        self.rgb_order = rgb_order
        self.disable_auto_write = disable_auto_write
        self.split = split
        self.rightSide = rightSide
        self.brightness_step = 0.1
        self.brightness = 0

        if name.endswith('L'):
            self.rightSide = False
        elif name.endswith('R'):
            self.rightSide = True
        if type(ledDisplay) is Rgb_matrix_data:
            self.ledDisplay = ledDisplay.data
        else:
            self.ledDisplay = ledDisplay

        make_key(
            names=('RGB_TOG',), on_press=self._rgb_tog, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_BRI',), on_press=self._rgb_bri, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_BRD',), on_press=self._rgb_brd, on_release=handler_passthrough
        )

    def _rgb_tog(self, *args, **kwargs):
        if self.enable:
            self.off()
        else:
            self.on()
        self.enable = not self.enable

    def _rgb_bri(self, *args, **kwargs):
        self.increase_brightness()

    def _rgb_brd(self, *args, **kwargs):
        self.decrease_brightness()

    def on(self):
        if self.neopixel:
            self.setBasedOffDisplay()
            self.neopixel.show()

    def off(self):
        if self.neopixel:
            self.set_rgb_fill((0, 0, 0))

    def set_rgb_fill(self, rgb):
        if self.neopixel:
            self.neopixel.fill(rgb)
            if self.disable_auto_write:
                self.neopixel.show()

    def set_brightness(self, brightness=None):
        if brightness is None:
            brightness = self.brightness

        if self.neopixel:
            self.neopixel.brightness = brightness
            if self.disable_auto_write:
                self.neopixel.show()

    def increase_brightness(self, step=None):
        if step is None:
            step = self.brightness_step

        self.brightness = (
            self.brightness + step if self.brightness + step <= 1.0 else 1.0
        )

        self.set_brightness(self.brightness)

    def decrease_brightness(self, step=None):
        if step is None:
            step = self.brightness_step

        self.brightness = (
            self.brightness - step if self.brightness - step >= 0.0 else 0.0
        )
        self.set_brightness(self.brightness)

    def setBasedOffDisplay(self):
        if self.split:
            for i, val in enumerate(self.ledDisplay):
                if self.rightSide:
                    if self.keyPos[i] >= (self.num_pixels / 2):
                        self.neopixel[int(self.keyPos[i] - (self.num_pixels / 2))] = (
                            val[0],
                            val[1],
                            val[2],
                        )
                else:
                    if self.keyPos[i] <= (self.num_pixels / 2):
                        self.neopixel[self.keyPos[i]] = (val[0], val[1], val[2])
        else:
            for i, val in enumerate(self.ledDisplay):
                self.neopixel[self.keyPos[i]] = (val[0], val[1], val[2])

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, board):
        self.neopixel = neopixel.NeoPixel(
            board.rgb_pixel_pin,
            board.num_pixels,
            brightness=board.brightness_limit,
            pixel_order=self.rgb_order,
            auto_write=not self.disable_auto_write,
        )
        self.num_pixels = board.num_pixels
        self.keyPos = board.led_key_pos
        self.brightness = board.brightness_limit
        self.on()
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        if self.neopixel:
            self.neopixel.brightness = (
                self.neopixel.brightness / 2
                if self.neopixel.brightness / 2 > 0
                else 0.1
            )
            if self.disable_auto_write:
                self.neopixel.show()

    def on_powersave_disable(self, sandbox):
        if self.neopixel:
            self.neopixel.brightness = self.brightness
            if self.disable_auto_write:
                self.neopixel.show()
