import time
from math import e, exp, pi, sin
from micropython import const

import pulseio

led_config = {
    'brightness_step': 5,
    'brightness_limit': 100,
    'breathe_center': 1.5,
    'animation_mode': 'static',
    'animation_speed': 1,
}

class led:
    brightness = 0
    time = int(time.monotonic() * 1000)
    pos = 0
    effect_init = False

    led = None
    brightness_step = 5
    brightness_limit = 100
    breathe_center = 1.5
    animation_mode = 'static'
    animation_speed = 1
    enabled = True

    def __init__(self, led_pin, config):
        self.led = pulseio.PWMOut(led_pin)
        self.brightness_step = const(config['brightness_step'])
        self.brightness_limit = const(config['brightness_limit'])
        self.animation_mode = const(config['animation_mode'])
        self.animation_speed = const(config['animation_speed'])
        self.breathe_center = const(config['breathe_center'])

    def __repr__(self):
        return 'LED({})'.format(self._to_dict())

    def _to_dict(self):
        return {
            'led': self.led,
            'brightness_step': self.brightness_step,
            'brightness_limit': self.brightness_limit,
            'animation_mode': self.animation_mode,
            'animation_speed': self.animation_speed,
            'breathe_center': self.breathe_center,
        }

    def _init_effect(self):
        self.pos = 0
        self.effect_init = False
        return self

    def time_ms(self):
        return int(time.monotonic() * 1000)

    def set_brightness(self, percent):
        self.led.duty_cycle = int(percent / 100 * 65535)

    def increase_brightness(self, step=None):
        if not step:
            self.brightness += self.brightness_step
        else:
            self.brightness += step

        if self.brightness > 100:
            self.brightness = 100

        self.set_brightness(self.brightness)

    def decrease_brightness(self, step=None):
        if not step:
            self.brightness -= self.brightness_step
        else:
            self.brightness -= step

        if self.brightness < 0:
            self.brightness = 0

        self.set_brightness(self.brightness)

    def off(self):
        self.set_brightness(0)

    def increase_ani(self):
        """
        Increases animation speed by 1 amount stopping at 10
        :param step:
        """
        if (self.animation_speed + 1) >= 10:
            self.animation_speed = 10
        else:
            self.val += 1

    def decrease_ani(self):
        """
        Decreases animation speed by 1 amount stopping at 0
        :param step:
        """
        if (self.val - 1) <= 0:
            self.val = 0
        else:
            self.val -= 1

    def effect_breathing(self):
        # http://sean.voisen.org/blog/2011/10/breathing-led-with-arduino/
        # https://github.com/qmk/qmk_firmware/blob/9f1d781fcb7129a07e671a46461e501e3f1ae59d/quantum/rgblight.c#L806
        self.brightness = int((exp(sin((self.pos / 255.0) * pi)) - self.breathe_center / e) *
                              (self.brightness_limit / (e - 1 / e)))
        self.pos = (self.pos + self.animation_speed) % 256
        self.set_brightness(self.brightness)

        return self

    def effect_static(self):
        self.set_brightness(self.brightness)
        # Set animation mode to none to prevent cycles from being wasted
        self.animation_mode = None
        return self

    def animate(self):
        """
        Activates a "step" in the animation based on the active mode
        :return: Returns the new state in animation
        """
        if self.effect_init:
            self._init_effect()
        if self.enabled:
            if self.animation_mode == 'breathing':
                return self.effect_breathing()
            elif self.animation_mode == 'static':
                return self.effect_static()
        else:
            self.off()

        return self
