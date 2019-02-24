import time
from math import e as M_E
from math import exp, floor, pi, sin


class RGB:
    hue = 0
    sat = 100
    val = 80
    pos = 0
    time = floor(time.monotonic() * 10)
    intervals = (30, 20, 10, 5)
    animation_speed = 1
    enabled = True
    neopixel = None
    rgbw = False
    reverse_animation = False
    disable_auto_write = False

    # Set by config
    num_pixels = 0
    hue_step = 10
    sat_step = 17
    val_step = 17
    breath_center = 1.5  # 1.0-2.7
    knight_effect_length = 4
    val_limit = 255
    animation_mode = 'static'
    effect_init = False

    def __init__(self, pixel_pin, rgb_order, num_pixels,
                 hue_step, sat_step, val_step,
                 hue_default, sat_default, val_default,
                 breath_center, knight_effect_length,
                 val_limit, animation_mode, animation_speed):
        try:
            import neopixel
            self.neopixel = neopixel.NeoPixel(pixel_pin,
                                              num_pixels,
                                              pixel_order=rgb_order,
                                              auto_write=False)
            if len(rgb_order) == 4:
                self.rgbw = True
            self.num_pixels = num_pixels
            self.hue_step = hue_step
            self.sat_step = sat_step
            self.val_step = val_step
            self.hue = hue_default
            self.sat = sat_default
            self.val = val_default
            self.breath_center = breath_center
            self.knight_effect_length = knight_effect_length
            self.val_limit = val_limit
            self.animation_mode = animation_mode
            self.animation_speed = animation_speed

        except ImportError as e:
            print(e)

    def __repr__(self):
        return 'RGB({})'.format(self._to_dict())

    def _to_dict(self):
        ret = {
            'hue': self.hue,
            'sat': self.sat,
            'val': self.val,
            'time': self.time,
            'intervals': self.intervals,
            'animation_mode': self.animation_mode,
            'animation_speed': self.animation_speed,
            'enabled': self.enabled,
            'neopixel': self.neopixel,
            'disable_auto_write': self.disable_auto_write,
        }

        return ret

    def time_ms(self):
        return floor(time.monotonic() * 10)

    def hsv_to_rgb(self, hue, sat, val):
        """
        Converts HSV values, and returns a tuple of RGB values
        :param hue:
        :param sat:
        :param val:
        :return: (r, g, b)
        """
        r = 0
        g = 0
        b = 0

        if val > self.val_limit:
            val = self.val_limit

        if sat == 0:
            r = val
            g = val
            b = val

        else:
            base = ((100 - sat) * val) / 100
            color = floor((val - base) * ((hue % 60) / 60))

            x = floor(hue / 60)
            if x == 0:
                r = val
                g = base + color
                b = base
            elif x == 1:
                r = val - color
                g = val
                b = base
            elif x == 2:
                r = base
                g = val
                b = base + color
            elif x == 3:
                r = base
                g = val - color
                b = val
            elif x == 4:
                r = base + color
                g = base
                b = val
            elif x == 5:
                r = val
                g = base
                b = val - color

        return floor(r), floor(g), floor(b)

    def hsv_to_rgbw(self, hue, sat, val):
        """
        Converts HSV values, and returns a tuple of RGBW values
        :param hue:
        :param sat:
        :param val:
        :return: (r, g, b, w)
        """
        rgb = self.hsv_to_rgb(hue, sat, val)
        return rgb[0], rgb[1], rgb[2], min(rgb)

    def set_hsv(self, hue, sat, val, index):
        """
        Takes HSV values and displays it on a single LED/Neopixel
        :param hue:
        :param sat:
        :param val:
        :param index: Index of LED/Pixel
        """
        if self.neopixel:
            if self.rgbw:
                self.set_rgb(self.hsv_to_rgbw(hue, sat, val), index)
            else:
                self.set_rgb(self.hsv_to_rgb(hue, sat, val), index)

    def set_hsv_fill(self, hue, sat, val):
        """
        Takes HSV values and displays it on all LEDs/Neopixels
        :param hue:
        :param sat:
        :param val:
        """
        if self.neopixel:
            if self.rgbw:
                self.set_rgb_fill(self.hsv_to_rgbw(hue, sat, val))
            else:
                self.set_rgb_fill(self.hsv_to_rgb(hue, sat, val))

    def set_rgb(self, rgb, index):
        """
        Takes an RGB or RGBW and displays it on a single LED/Neopixel
        :param rgb: RGB or RGBW
        :param index: Index of LED/Pixel
        """
        if self.neopixel and 0 <= index <= self.num_pixels - 1:
            self.neopixel[index] = rgb
            if not self.disable_auto_write:
                self.neopixel.show()

    def set_rgb_fill(self, rgb):
        """
        Takes an RGB or RGBW and displays it on all LEDs/Neopixels
        :param rgb: RGB or RGBW
        """
        if self.neopixel:
            self.neopixel.fill(rgb)
            if not self.disable_auto_write:
                self.neopixel.show()

    def increase_hue(self, step):
        """
        Increases hue by step amount rolling at 360 and returning to 0
        :param step:
        """
        self.hue = (self.hue + step) % 360

    def decrease_hue(self, step):
        """
        Decreases hue by step amount rolling at 0 and returning to 360
        :param step:
        """
        if (self.hue - step) <= 0:
            self.hue = (self.hue + 360 - step) % 360
        else:
            self.hue = (self.hue - step) % 360

    def increase_sat(self, step):
        """
        Increases saturation by step amount stopping at 100
        :param step:
        """
        if self.sat + step >= 100:
            self.sat = 100
        else:
            self.sat += step

    def decrease_sat(self, step):
        """
        Decreases saturation by step amount stopping at 0
        :param step:
        """
        if (self.sat - step) <= 0:
            self.sat = 0
        else:
            self.sat -= step

    def increase_val(self, step):
        """
        Increases value by step amount stopping at 100
        :param step:
        """
        if (self.val + step) >= 100:
            self.val = 100
        else:
            self.val += step

    def decrease_val(self, step):
        """
        Decreases value by step amount stopping at 0
        :param step:
        """
        if (self.val - step) <= 0:
            self.val = 0
        else:
            self.val -= step

    def off(self):
        """
        Turns off all LEDs/Neopixels without changing stored values
        """
        if self.neopixel:
            self.set_hsv_fill(0, 0, 0)

    def show(self):
        """
        Turns on all LEDs/Neopixels without changing stored values
        """
        if self.neopixel:
            self.neopixel.show()

    def animate(self):
        """
        Activates a "step" in the animation based on the active mode
        :return: Returns the new state in animation
        """
        if self.effect_init:
            self.init_effect()
        if self.enabled:
            if self.animation_mode == 'breathing':
                return self.effect_breathing()
            elif self.animation_mode == 'rainbow':
                return self.effect_rainbow()
            elif self.animation_mode == 'breathing_rainbow':
                return self.effect_breathing_rainbow()
            elif self.animation_mode == 'static':
                return self.effect_static()
            elif self.animation_mode == 'knight':
                return self.effect_knight()
        else:
            self.off()

        return self

    def animation_step(self):
        interval = self.time_ms() - self.time
        if interval >= max(self.intervals):
            self.time = self.time_ms()
            return max(self.intervals)
        if interval in self.intervals:
            return interval
        else:
            return False

    def init_effect(self):
        self.pos = 0
        self.reverse_animation = False
        self.effect_init = False

    def effect_static(self):
        self.set_hsv_fill(self.hue, self.sat, self.val)
        return self

    def effect_breathing(self):
        # http://sean.voisen.org/blog/2011/10/breathing-led-with-arduino/
        # https://github.com/qmk/qmk_firmware/blob/9f1d781fcb7129a07e671a46461e501e3f1ae59d/quantum/rgblight.c#L806
        self.val = floor((exp(sin((self.pos / 255.0) * pi)) - self.breath_center / M_E) *
                         (self.val_limit / (M_E - 1 / M_E)))
        self.pos = (self.pos + self.animation_speed) % 256
        self.set_hsv_fill(self.hue, self.sat, self.val)

        return self

    def effect_breathing_rainbow(self):
        if self.animation_step():
            self.increase_hue(self.animation_speed)
        self.effect_breathing()

        return self

    def effect_rainbow(self):
        if self.animation_step():
            self.increase_hue(self.animation_speed)
            self.set_hsv_fill(self.hue, self.sat, self.val)

        return self

    def effect_knight(self):
        # Determine which LEDs should be lit up
        self.disable_auto_write = True  # Turn off instantly showing
        self.off()  # Fill all off
        pos = floor(self.pos)

        # Set all pixels on in range of animation length offset by position
        for i in range(pos, (pos + self.knight_effect_length)):
            self.set_hsv(self.hue, self.sat, self.val, i)

        # Reverse animation when a boundary is hit
        if pos >= self.num_pixels or pos - 1 < (self.knight_effect_length * -1):
            self.reverse_animation = not self.reverse_animation

        if self.reverse_animation:
            self.pos -= self.animation_speed / 5
        else:
            self.pos += self.animation_speed / 5

        # Show final results
        self.disable_auto_write = False  # Resume showing changes
        self.show()

        return self
