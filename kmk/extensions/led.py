import pwmio
from math import e, exp, pi, sin

from kmk.extensions import Extension, InvalidExtensionEnvironment
from kmk.keys import make_argumented_key, make_key
from kmk.utils import clamp


class LEDKeyMeta:
    def __init__(self, *leds):
        self.leds = leds
        self.brightness = None


class AnimationModes:
    OFF = 0
    STATIC = 1
    STATIC_STANDBY = 2
    BREATHING = 3
    USER = 4


class LED(Extension):
    def __init__(
        self,
        led_pin,
        brightness_step=5,
        brightness_limit=100,
        breathe_center=1.5,
        animation_mode=AnimationModes.STATIC,
        animation_speed=1,
        user_animation=None,
        val=100,
    ):
        try:
            pins_iter = iter(led_pin)
        except TypeError:
            pins_iter = [led_pin]

        try:
            self._leds = [pwmio.PWMOut(pin) for pin in pins_iter]
        except Exception as e:
            print(e)
            raise InvalidExtensionEnvironment(
                'Unable to create pwmio.PWMOut() instance with provided led_pin'
            )

        self._brightness = 0
        self._pos = 0
        self._effect_init = False
        self._enabled = True

        self.brightness_step = brightness_step
        self.brightness_limit = brightness_limit
        self.animation_mode = animation_mode
        self.animation_speed = animation_speed
        self.breathe_center = breathe_center
        self.val = val

        if user_animation is not None:
            self.user_animation = user_animation

        make_argumented_key(
            names=('LED_TOG',),
            validator=self._led_key_validator,
            on_press=self._key_led_tog,
        )
        make_argumented_key(
            names=('LED_INC',),
            validator=self._led_key_validator,
            on_press=self._key_led_inc,
        )
        make_argumented_key(
            names=('LED_DEC',),
            validator=self._led_key_validator,
            on_press=self._key_led_dec,
        )
        make_argumented_key(
            names=('LED_SET',),
            validator=self._led_set_key_validator,
            on_press=self._key_led_set,
        )
        make_key(names=('LED_ANI',), on_press=self._key_led_ani)
        make_key(names=('LED_AND',), on_press=self._key_led_and)
        make_key(
            names=('LED_MODE_PLAIN', 'LED_M_P'), on_press=self._key_led_mode_static
        )
        make_key(
            names=('LED_MODE_BREATHE', 'LED_M_B'), on_press=self._key_led_mode_breathe
        )

    def __repr__(self):
        return f'LED({self._to_dict()})'

    def _to_dict(self):
        return {
            '_brightness': self._brightness,
            '_pos': self._pos,
            'brightness_step': self.brightness_step,
            'brightness_limit': self.brightness_limit,
            'animation_mode': self.animation_mode,
            'animation_speed': self.animation_speed,
            'breathe_center': self.breathe_center,
            'val': self.val,
        }

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
        if self._enabled and self.animation_mode:
            self.animate()
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return

    def _init_effect(self):
        self._pos = 0
        self._effect_init = False
        return self

    def set_brightness(self, percent, leds=None):
        leds = leds or range(0, len(self._leds))
        for i in leds:
            self._leds[i].duty_cycle = int(percent / 100 * 65535)

    def step_brightness(self, step, leds=None):
        leds = leds or range(0, len(self._leds))
        for i in leds:
            brightness = int(self._leds[i].duty_cycle / 65535 * 100) + step
            self.set_brightness(clamp(brightness), [i])

    def increase_brightness(self, step=None, leds=None):
        if step is None:
            step = self.brightness_step
        self.step_brightness(step, leds)

    def decrease_brightness(self, step=None, leds=None):
        if step is None:
            step = self.brightness_step
        self.step_brightness(-step, leds)

    def off(self):
        self.set_brightness(0)

    def increase_ani(self):
        '''
        Increases animation speed by 1 amount stopping at 10
        :param step:
        '''
        if (self.animation_speed + 1) >= 10:
            self.animation_speed = 10
        else:
            self.val += 1

    def decrease_ani(self):
        '''
        Decreases animation speed by 1 amount stopping at 0
        :param step:
        '''
        if (self.val - 1) <= 0:
            self.val = 0
        else:
            self.val -= 1

    def effect_breathing(self):
        # http://sean.voisen.org/blog/2011/10/breathing-led-with-arduino/
        # https://github.com/qmk/qmk_firmware/blob/9f1d781fcb7129a07e671a46461e501e3f1ae59d/quantum/rgblight.c#L806
        sined = sin((self._pos / 255.0) * pi)
        multip_1 = exp(sined) - self.breathe_center / e
        multip_2 = self.brightness_limit / (e - 1 / e)

        self._brightness = int(multip_1 * multip_2)
        self._pos = (self._pos + self.animation_speed) % 256
        self.set_brightness(self._brightness)

    def effect_static(self):
        self.set_brightness(self._brightness)
        # Set animation mode to none to prevent cycles from being wasted
        self.animation_mode = None

    def animate(self):
        '''
        Activates a "step" in the animation based on the active mode
        :return: Returns the new state in animation
        '''
        if self._effect_init:
            self._init_effect()
        if self._enabled:
            if self.animation_mode == AnimationModes.BREATHING:
                return self.effect_breathing()
            elif self.animation_mode == AnimationModes.STATIC:
                return self.effect_static()
            elif self.animation_mode == AnimationModes.USER:
                return self.user_animation(self)
        else:
            self.off()

    def _led_key_validator(self, *leds):
        if leds:
            for led in leds:
                assert self._leds[led]
        return LEDKeyMeta(*leds)

    def _led_set_key_validator(self, brightness, *leds):
        meta = self._led_key_validator(*leds)
        meta.brightness = brightness
        return meta

    def _key_led_tog(self, *args, **kwargs):
        if self.animation_mode == AnimationModes.STATIC_STANDBY:
            self.animation_mode = AnimationModes.STATIC

        self._enabled = not self._enabled

    def _key_led_inc(self, key, *args, **kwargs):
        self.increase_brightness(leds=key.meta.leds)

    def _key_led_dec(self, key, *args, **kwargs):
        self.decrease_brightness(leds=key.meta.leds)

    def _key_led_set(self, key, *args, **kwargs):
        self.set_brightness(percent=key.meta.brightness, leds=key.meta.leds)

    def _key_led_ani(self, *args, **kwargs):
        self.increase_ani()

    def _key_led_and(self, *args, **kwargs):
        self.decrease_ani()

    def _key_led_mode_static(self, *args, **kwargs):
        self._effect_init = True
        self.animation_mode = AnimationModes.STATIC

    def _key_led_mode_breathe(self, *args, **kwargs):
        self._effect_init = True
        self.animation_mode = AnimationModes.BREATHING
