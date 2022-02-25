import neopixel
from supervisor import ticks_ms

from math import e, exp, pi, sin

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key

rgb_config = {}


class AnimationModes:
    OFF = 0
    STATIC = 1
    STATIC_STANDBY = 2
    BREATHING = 3
    RAINBOW = 4
    BREATHING_RAINBOW = 5
    KNIGHT = 6
    SWIRL = 7
    USER = 8


class RGB(Extension):
    pos = 0

    def __init__(
        self,
        pixel_pin,
        num_pixels=0,
        val_limit=100,
        hue_default=0,
        sat_default=100,
        rgb_order=(1, 0, 2),  # GRB WS2812
        val_default=100,
        hue_step=5,
        sat_step=5,
        val_step=5,
        animation_speed=1,
        breathe_center=1,  # 1.0-2.7
        knight_effect_length=3,
        animation_mode=AnimationModes.STATIC,
        effect_init=False,
        reverse_animation=False,
        user_animation=None,
        disable_auto_write=False,
        pixels=None,
        refresh_rate=60,
    ):
        if pixels is None:
            self.pixels = neopixel.NeoPixel(
                pixel_pin,
                num_pixels,
                pixel_order=rgb_order,
                auto_write=not disable_auto_write,
            )
        else:
            self.pixels = pixels

        self.rgbw = bool(len(rgb_order) == 4)

        self.num_pixels = num_pixels
        self.hue_step = hue_step
        self.sat_step = sat_step
        self.val_step = val_step
        self.hue = hue_default
        self.hue_default = hue_default
        self.sat = sat_default
        self.sat_default = sat_default
        self.val = val_default
        self.val_default = val_default
        self.breathe_center = breathe_center
        self.knight_effect_length = knight_effect_length
        self.val_limit = val_limit
        self.animation_mode = animation_mode
        self.animation_speed = animation_speed
        self.effect_init = effect_init
        self.reverse_animation = reverse_animation
        self.user_animation = user_animation
        self.disable_auto_write = disable_auto_write
        self.refresh_rate = refresh_rate

        self._substep = 0
        self._time = ticks_ms()

        make_key(
            names=('RGB_TOG',), on_press=self._rgb_tog, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_HUI',), on_press=self._rgb_hui, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_HUD',), on_press=self._rgb_hud, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_SAI',), on_press=self._rgb_sai, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_SAD',), on_press=self._rgb_sad, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_VAI',), on_press=self._rgb_vai, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_VAD',), on_press=self._rgb_vad, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_ANI',), on_press=self._rgb_ani, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_AND',), on_press=self._rgb_and, on_release=handler_passthrough
        )
        make_key(
            names=('RGB_MODE_PLAIN', 'RGB_M_P'),
            on_press=self._rgb_mode_static,
            on_release=handler_passthrough,
        )
        make_key(
            names=('RGB_MODE_BREATHE', 'RGB_M_B'),
            on_press=self._rgb_mode_breathe,
            on_release=handler_passthrough,
        )
        make_key(
            names=('RGB_MODE_RAINBOW', 'RGB_M_R'),
            on_press=self._rgb_mode_rainbow,
            on_release=handler_passthrough,
        )
        make_key(
            names=('RGB_MODE_BREATHE_RAINBOW', 'RGB_M_BR'),
            on_press=self._rgb_mode_breathe_rainbow,
            on_release=handler_passthrough,
        )
        make_key(
            names=('RGB_MODE_SWIRL', 'RGB_M_S'),
            on_press=self._rgb_mode_swirl,
            on_release=handler_passthrough,
        )
        make_key(
            names=('RGB_MODE_KNIGHT', 'RGB_M_K'),
            on_press=self._rgb_mode_knight,
            on_release=handler_passthrough,
        )
        make_key(
            names=('RGB_RESET', 'RGB_RST'),
            on_press=self._rgb_reset,
            on_release=handler_passthrough,
        )

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        self.animate()

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        self._do_update()

    def hsv_to_rgb(self, hue, sat, val):
        '''
        Converts HSV values, and returns a tuple of RGB values
        :param hue:
        :param sat:
        :param val:
        :return: (r, g, b)
        '''
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
            color = (val - base) * ((hue % 60) / 60)

            x = int(hue / 60)
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

        return int(r), int(g), int(b)

    def hsv_to_rgbw(self, hue, sat, val):
        '''
        Converts HSV values, and returns a tuple of RGBW values
        :param hue:
        :param sat:
        :param val:
        :return: (r, g, b, w)
        '''
        rgb = self.hsv_to_rgb(hue, sat, val)
        return rgb[0], rgb[1], rgb[2], min(rgb)

    def set_hsv(self, hue, sat, val, index):
        '''
        Takes HSV values and displays it on a single LED/Neopixel
        :param hue:
        :param sat:
        :param val:
        :param index: Index of LED/Pixel
        '''
        if self.pixels:
            if self.rgbw:
                self.set_rgb(self.hsv_to_rgbw(hue, sat, val), index)
            else:
                self.set_rgb(self.hsv_to_rgb(hue, sat, val), index)

    def set_hsv_fill(self, hue, sat, val):
        '''
        Takes HSV values and displays it on all LEDs/Neopixels
        :param hue:
        :param sat:
        :param val:
        '''
        if self.pixels:
            if self.rgbw:
                self.set_rgb_fill(self.hsv_to_rgbw(hue, sat, val))
            else:
                self.set_rgb_fill(self.hsv_to_rgb(hue, sat, val))

    def set_rgb(self, rgb, index):
        '''
        Takes an RGB or RGBW and displays it on a single LED/Neopixel
        :param rgb: RGB or RGBW
        :param index: Index of LED/Pixel
        '''
        if self.pixels and 0 <= index <= self.num_pixels - 1:
            self.pixels[index] = rgb
            if not self.disable_auto_write:
                self.pixels.show()

    def set_rgb_fill(self, rgb):
        '''
        Takes an RGB or RGBW and displays it on all LEDs/Neopixels
        :param rgb: RGB or RGBW
        '''
        if self.pixels:
            self.pixels.fill(rgb)
            if not self.disable_auto_write:
                self.pixels.show()

    def increase_hue(self, step=None):
        '''
        Increases hue by step amount rolling at 360 and returning to 0
        :param step:
        '''
        if step is None:
            step = self.hue_step

        self.hue = (self.hue + step) % 360

        if self._check_update():
            self._do_update()

    def decrease_hue(self, step=None):
        '''
        Decreases hue by step amount rolling at 0 and returning to 360
        :param step:
        '''
        if step is None:
            step = self.hue_step

        if (self.hue - step) <= 0:
            self.hue = (self.hue + 360 - step) % 360
        else:
            self.hue = (self.hue - step) % 360

        if self._check_update():
            self._do_update()

    def increase_sat(self, step=None):
        '''
        Increases saturation by step amount stopping at 100
        :param step:
        '''
        if step is None:
            step = self.sat_step

        if self.sat + step >= 100:
            self.sat = 100
        else:
            self.sat += step

        if self._check_update():
            self._do_update()

    def decrease_sat(self, step=None):
        '''
        Decreases saturation by step amount stopping at 0
        :param step:
        '''
        if step is None:
            step = self.sat_step

        if (self.sat - step) <= 0:
            self.sat = 0
        else:
            self.sat -= step

        if self._check_update():
            self._do_update()

    def increase_val(self, step=None):
        '''
        Increases value by step amount stopping at 100
        :param step:
        '''
        if step is None:
            step = self.val_step
        if (self.val + step) >= 100:
            self.val = 100
        else:
            self.val += step

        if self._check_update():
            self._do_update()

    def decrease_val(self, step=None):
        '''
        Decreases value by step amount stopping at 0
        :param step:
        '''
        if step is None:
            step = self.val_step
        if (self.val - step) <= 0:
            self.val = 0
        else:
            self.val -= step

        if self._check_update():
            self._do_update()

    def increase_ani(self):
        '''
        Increases animation speed by 1 amount stopping at 10
        :param step:
        '''
        if (self.animation_speed + 1) > 10:
            self.animation_speed = 10
        else:
            self.animation_speed += 1
        if self._check_update():
            self._do_update()

    def decrease_ani(self):
        '''
        Decreases animation speed by 1 amount stopping at 0
        :param step:
        '''
        if (self.animation_speed - 1) <= 0:
            self.animation_speed = 0
        else:
            self.animation_speed -= 1
        if self._check_update():
            self._do_update()

    def off(self):
        '''
        Turns off all LEDs/Neopixels without changing stored values
        '''
        if self.pixels:
            self.set_hsv_fill(0, 0, 0)

    def show(self):
        '''
        Turns on all LEDs/Neopixels without changing stored values
        '''
        if self.pixels:
            self.pixels.show()

    def animate(self):
        '''
        Activates a "step" in the animation based on the active mode
        :return: Returns the new state in animation
        '''
        if self.effect_init:
            self._init_effect()

        if self.animation_mode is AnimationModes.STATIC_STANDBY:
            return

        now = ticks_ms()
        if self.enable and now - self._time > (1000 // self.refresh_rate):
            self._time = now
            self._animation_step()
            if self.animation_mode == AnimationModes.BREATHING:
                self.effect_breathing()
            elif self.animation_mode == AnimationModes.RAINBOW:
                self.effect_rainbow()
            elif self.animation_mode == AnimationModes.BREATHING_RAINBOW:
                self.effect_breathing_rainbow()
            elif self.animation_mode == AnimationModes.STATIC:
                self.effect_static()
            elif self.animation_mode == AnimationModes.KNIGHT:
                self.effect_knight()
            elif self.animation_mode == AnimationModes.SWIRL:
                self.effect_swirl()
            elif self.animation_mode == AnimationModes.USER:
                self.user_animation(self)
            elif self.animation_mode == AnimationModes.STATIC_STANDBY:
                pass
            else:
                self.off()

    def _animation_step(self):
        self._substep += self.animation_speed / 4
        self._step = int(self._substep)
        self._substep -= self._step

    def _init_effect(self):
        self.pos = 0
        self.reverse_animation = False
        self.effect_init = False

    def _check_update(self):
        return bool(self.animation_mode == AnimationModes.STATIC_STANDBY)

    def _do_update(self):
        if self.animation_mode == AnimationModes.STATIC_STANDBY:
            self.animation_mode = AnimationModes.STATIC

    def effect_static(self):
        self.set_hsv_fill(self.hue, self.sat, self.val)
        self.animation_mode = AnimationModes.STATIC_STANDBY

    def effect_breathing(self):
        # http://sean.voisen.org/blog/2011/10/breathing-led-with-arduino/
        # https://github.com/qmk/qmk_firmware/blob/9f1d781fcb7129a07e671a46461e501e3f1ae59d/quantum/rgblight.c#L806
        sined = sin((self.pos / 255.0) * pi)
        multip_1 = exp(sined) - self.breathe_center / e
        multip_2 = self.val_limit / (e - 1 / e)

        self.val = int(multip_1 * multip_2)
        self.pos = (self.pos + self._step) % 256
        self.set_hsv_fill(self.hue, self.sat, self.val)

    def effect_breathing_rainbow(self):
        self.increase_hue(self._step)
        self.effect_breathing()

    def effect_rainbow(self):
        self.increase_hue(self._step)
        self.set_hsv_fill(self.hue, self.sat, self.val)

    def effect_swirl(self):
        print('.', ticks_ms() % 1000, self.animation_speed, self._step)
        self.increase_hue(self._step)
        self.disable_auto_write = True  # Turn off instantly showing
        for i in range(0, self.num_pixels):
            self.set_hsv(
                (self.hue - (i * self.num_pixels)) % 360, self.sat, self.val, i
            )

        # Show final results
        self.disable_auto_write = False  # Resume showing changes
        self.show()

    def effect_knight(self):
        # Determine which LEDs should be lit up
        self.disable_auto_write = True  # Turn off instantly showing
        self.off()  # Fill all off
        pos = int(self.pos)

        # Set all pixels on in range of animation length offset by position
        for i in range(pos, (pos + self.knight_effect_length)):
            self.set_hsv(self.hue, self.sat, self.val, i)

        # Reverse animation when a boundary is hit
        if pos >= self.num_pixels or pos - 1 < (self.knight_effect_length * -1):
            self.reverse_animation = not self.reverse_animation

        if self.reverse_animation:
            self.pos -= self._step / 2
        else:
            self.pos += self._step / 2

        # Show final results
        self.disable_auto_write = False  # Resume showing changes
        self.show()

    def _rgb_tog(self, *args, **kwargs):
        if self.animation_mode == AnimationModes.STATIC:
            self.animation_mode = AnimationModes.STATIC_STANDBY
            self._do_update()
        if self.animation_mode == AnimationModes.STATIC_STANDBY:
            self.animation_mode = AnimationModes.STATIC
            self._do_update()
        if self.enable:
            self.off()
        self.enable = not self.enable

    def _rgb_hui(self, *args, **kwargs):
        self.increase_hue()

    def _rgb_hud(self, *args, **kwargs):
        self.decrease_hue()

    def _rgb_sai(self, *args, **kwargs):
        self.increase_sat()

    def _rgb_sad(self, *args, **kwargs):
        self.decrease_sat()

    def _rgb_vai(self, *args, **kwargs):
        self.increase_val()

    def _rgb_vad(self, *args, **kwargs):
        self.decrease_val()

    def _rgb_ani(self, *args, **kwargs):
        self.increase_ani()

    def _rgb_and(self, *args, **kwargs):
        self.decrease_ani()

    def _rgb_mode_static(self, *args, **kwargs):
        self.effect_init = True
        self.animation_mode = AnimationModes.STATIC

    def _rgb_mode_breathe(self, *args, **kwargs):
        self.effect_init = True
        self.animation_mode = AnimationModes.BREATHING

    def _rgb_mode_breathe_rainbow(self, *args, **kwargs):
        self.effect_init = True
        self.animation_mode = AnimationModes.BREATHING_RAINBOW

    def _rgb_mode_rainbow(self, *args, **kwargs):
        self.effect_init = True
        self.animation_mode = AnimationModes.RAINBOW

    def _rgb_mode_swirl(self, *args, **kwargs):
        self.effect_init = True
        self.animation_mode = AnimationModes.SWIRL

    def _rgb_mode_knight(self, *args, **kwargs):
        self.effect_init = True
        self.animation_mode = AnimationModes.KNIGHT

    def _rgb_reset(self, *args, **kwargs):
        self.hue = self.hue_default
        self.sat = self.sat_default
        self.val = self.val_default
        if self.animation_mode == AnimationModes.STATIC_STANDBY:
            self.animation_mode = AnimationModes.STATIC
        self._do_update()
