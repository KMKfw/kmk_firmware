from math import e, exp, pi, sin, floor, atan2
from random import randint

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key
from kmk.scheduler import create_task
from kmk.utils import Debug, clamp
import time

debug = Debug(__name__)


class Timing:
    WALL = 0
    FRAME = 1


def hsv_to_rgb(hue, sat, val):
    '''
    Converts HSV values, and returns a tuple of RGB values
    :param hue:
    :param sat:
    :param val:
    :return: (r, g, b)
    '''
    if sat == 0:
        return (val, val, val)

    hue = 6 * (hue & 0xFF)
    frac = hue & 0xFF
    sxt = hue >> 8

    base = (0xFF - sat) * val
    color = (val * sat * frac) >> 8
    val <<= 8

    if sxt == 0:
        r = val
        g = base + color
        b = base
    elif sxt == 1:
        r = val - color
        g = val
        b = base
    elif sxt == 2:
        r = base
        g = val
        b = base + color
    elif sxt == 3:
        r = base
        g = val - color
        b = val
    elif sxt == 4:
        r = base + color
        g = base
        b = val
    elif sxt == 5:
        r = val
        g = base
        b = val - color

    return (r >> 8), (g >> 8), (b >> 8)


def effect_larson_scan(self):
    def animate(t):
        offset = (sin(t * pi * 2) + 1) / 2.0

        falloff = 2.4
        max_val = self._width - 1

        offset = int(round(offset * max_val))

        for y in range(self._height):
            for x in range(self._width):
                val = max_val - (abs(offset - x) * falloff)
                val /= max_val
                val = max(val, 0.0)
                self.set_hsv(x, y, self.hue, self.sat, int(self.val * val))

    return animate


def effect_breathe(self, breathe_center=1.0):
    multip_2 = clamp(self.val, 0, self.val) / (e - 1 / e)

    def animate(t):
        # http://sean.voisen.org/blog/2011/10/breathing-led-with-arduino/
        # https://github.com/qmk/qmk_firmware/blob/9f1d781fcb7129a07e671a46461e501e3f1ae59d/quantum/rgblight.c#L806
        multip_1 = exp(sin(t * pi)) - breathe_center / e

        self.set_hsv_fill(self.hue, self.sat, int(multip_1 * multip_2))

    return animate


class Orientation:
    VERTICAL = 0
    HORIZONTAL = 1


def effect_wave(self, breathe_center=1.0, spread=20, orientation=Orientation.VERTICAL):
    multip_2 = clamp(self.val, 0, self.val) / (e - 1 / e)
    spread /= pi

    def animate_v(t):
        for y in range(self._height):
            multip_1 = exp(sin((t + y * spread) * pi)) - breathe_center / e
            for x in range(self._width):
                self.set_hsv(x, y, self.hue, self.sat, int(multip_1 * multip_2))

    def animate_h(t):
        for x in range(self._width):
            multip_1 = exp(sin((t + x * spread) * pi)) - breathe_center / e
            for y in range(self._height):
                self.set_hsv(x, y, self.hue, self.sat, int(multip_1 * multip_2))

    return animate_h if orientation == Orientation.HORIZONTAL else animate_v


def effect_cycle(self, duration=30):
    # Number of seconds to complete a full cycle at 1.0 speed
    duration = 255.0 / duration

    def animate(t):
        hue = int(self.hue + (t * duration)) % 255
        self.set_hsv_fill(hue, self.sat, self.val)

    return animate


def effect_rainbow(self, duration=15, spread=None, orientation=Orientation.VERTICAL):
    # Number of seconds to complete a full cycle at 1.0 speed
    duration = 255.0 / duration

    m = self._width if orientation == Orientation.HORIZONTAL else self._height
    spread = 255 / m / 4.0 if spread is None else spread

    def animate_v(t):
        for y in range(self._height):
            hue = int(self.hue + (t * duration) + y *spread) % 255
            for x in range(self._width):
                self.set_hsv(x, y, hue, self.sat, self.val)

    def animate_h(t):
        for x in range(self._width):
            hue = int(self.hue + (t * duration) + x * spread) % 255
            for y in range(self._height):
                self.set_hsv(x, y, hue, self.sat, self.val)

    return animate_h if orientation == Orientation.HORIZONTAL else animate_v


def effect_rainbow_candy(self, duration=30, spread=10.0):
    # Number of seconds to complete a full cycle at 1.0 speed
    duration = 255.0 / duration

    def animate(t):
        hue = self.hue + (t * duration)
        for y in range(self._height):
            for x in range(self._width):
                self.set_hsv(x, y, int(hue) % 255, self.sat, self.val)
                hue += spread

    return animate


def effect_rainbow_random(self, duration=10):
    # Number of seconds to complete a full cycle at 1.0 speed
    duration = 255.0 / duration

    count = self._width * self._height
    offsets = [randint(0, 255) for _ in range(count)]

    def animate(t):
        hue = self.hue + (t * duration)
        i = 0
        for y in range(self._height):
            for x in range(self._width):
                self.set_hsv(x, y, int(hue + offsets[i]) % 255, self.sat, self.val)
                i += 1

    return animate


def effect_spin(self, duration=5):
    # Number of seconds to complete a full cycle at 1.0 speed
    duration = 255.0 / duration

    c_x = self._width / 2.0
    c_y = self._height / 2.0

    def animate(t):
        hue = self.hue + (t * duration)

        for y in range(self._height):
            for x in range(self._width):
                a = atan2(c_y - y, c_x - x) / pi * 128
                self.set_hsv(x, y, int(hue + a), self.sat, self.val)

    return animate


class RGB2D(Extension):
    pos = 0

    def __init__(
        self,
        pixels,
        effect = None,
        width = None,
        height = None,
        refresh_rate=60,
        timing = Timing.WALL
    ):
        self.pixels = pixels
        self._width = width if width else pixels.width
        self._height = height if height else pixels.height
        self._refresh_rate = refresh_rate
        self._animation_speed = 1.0
        self._frame = 0
        self._timing = timing

        self.hue = 120
        self.sat = 255
        self.val = 255

        self._effect = effect(self) if effect else effect_spin(self)

        self._total_time = 0

    def update_effect(self, effect):
        self._effect = effect(self)

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):

        # Turn off auto_write on the backend.
        # We handle the propagation of auto_write behaviour.
        self.pixels.auto_write = False

        self._task = create_task(self.animate, period_ms=(1000 // self._refresh_rate))

    def before_matrix_scan(self, sandbox):
        return
    
    def process_key(self, keyboard, key, is_pressed, int_coord):
        return key

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        pass

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        self._do_update()

    def deinit(self, sandbox):
        self.pixels.deinit()

    def set_hsv(self, x, y, hue, sat, val):
        '''
        Takes HSV values and displays it on a single LED
        :param x:
        :param y:
        :param hue:
        :param sat:
        :param val:
        :param index: Index of LED/Pixel
        '''
        self.set_rgb(x, y, hsv_to_rgb(hue, sat, val))

    def set_hsv_fill(self, hue, sat, val):
        '''
        Takes HSV values and displays it on all LEDs
        :param hue:
        :param sat:
        :param val:
        '''
        self.pixels.fill(hsv_to_rgb(hue, sat, val))

    def set_rgb(self, x, y, rgb):
        '''
        Takes an RGB or RGBW and displays it on a single LED
        :param x:
        :param y:
        :param rgb: RGB or RGBW
        :param index: Index of LED/Pixel
        '''
        index = y * self._height + x
        try:
            self.pixels[index] = rgb
        except IndexError:
            pass

    def set_rgb_fill(self, rgb):
        '''
        Takes an RGB or RGBW and displays it on all LEDs
        :param rgb: RGB or RGBW
        '''
        self.pixels.fill(rgb)

    def clear(self):
        self.pixels.fill((0, 0, 0))

    def animate(self):
        '''
        Activates a "step" in the animation based on the active mode
        :return: Returns the new state in animation
        '''
        t_start = time.monotonic()

        if self._timing == Timing.WALL:
            # wall clock timing
            t = time.monotonic() * self._animation_speed
        else:
            # frame counting
            t = (self._frame / self._refresh_rate) * self._animation_speed

        self._effect(t)

        self.pixels.show()
        self._frame += 1

        if debug.enabled:
            t_end = time.monotonic()
            self._total_time += t_end - t_start
            frames = 240
            if self._frame > 0 and self._frame % frames == 0:
                avg_time = self._total_time / frames
                print(f"Effect {frames} frame avg: {avg_time * 1000:.4f}ms ({1.0 / avg_time:.2f} FPS)")
                self._total_time = 0
