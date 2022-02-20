# Use this extension for showing layer status with three leds

import pwmio
import time

from kmk.extensions import Extension, InvalidExtensionEnvironment
from kmk.keys import make_key


class statusLED(Extension):
    def __init__(
        self,
        led_pins,
        brightness=30,
        brightness_step=5,
        brightness_limit=100,
    ):
        self._leds = []
        for led in led_pins:
            try:
                self._leds.append(pwmio.PWMOut(led))
            except Exception as e:
                print(e)
                raise InvalidExtensionEnvironment(
                    'Unable to create pulseio.PWMOut() instance with provided led_pin'
                )
        self._led_count = len(self._leds)

        self.brightness = brightness
        self._layer_last = -1

        self.brightness_step = brightness_step
        self.brightness_limit = brightness_limit

        make_key(names=('SLED_INC',), on_press=self._key_led_inc)
        make_key(names=('SLED_DEC',), on_press=self._key_led_dec)

    def _layer_indicator(self, layer_active, *args, **kwargs):
        '''
        Indicates layer with leds

        For the time being just a simple consecutive single led
        indicator. And when there are more layers than leds it
        wraps around to the first led again.
        (Also works for a single led, which just lights when any
        layer is active)
        '''

        if self._layer_last != layer_active:
            led_last = 0 if self._layer_last == 0 else 1 + (self._layer_last - 1) % 3
            if layer_active > 0:
                led_active = 0 if layer_active == 0 else 1 + (layer_active - 1) % 3
                self.set_brightness(self.brightness, led_active)
                self.set_brightness(0, led_last)
            else:
                self.set_brightness(0, led_last)
            self._layer_last = layer_active

    def __repr__(self):
        return 'SLED({})'.format(self._to_dict())

    def _to_dict(self):
        return {
            '_brightness': self.brightness,
            'brightness_step': self.brightness_step,
            'brightness_limit': self.brightness_limit,
        }

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        '''Light up every single led once for 200 ms'''
        for i in range(self._led_count + 2):
            if i < self._led_count:
                self._leds[i].duty_cycle = int(self.brightness / 100 * 65535)
            i_off = i - 2
            if i_off >= 0 and i_off < self._led_count:
                self._leds[i_off].duty_cycle = int(0)
            time.sleep(0.1)
        for led in self._leds:
            led.duty_cycle = int(0)
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        self._layer_indicator(sandbox.active_layers[0])
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        self.set_brightness(0)
        return

    def on_powersave_disable(self, sandbox):
        self.set_brightness(self._brightness)
        self._leds[2].duty_cycle = int(50 / 100 * 65535)
        time.sleep(0.2)
        self._leds[2].duty_cycle = int(0)
        return

    def set_brightness(self, percent, layer_id=-1):
        if layer_id < 0:
            for led in self._leds:
                led.duty_cycle = int(percent / 100 * 65535)
        else:
            self._leds[layer_id - 1].duty_cycle = int(percent / 100 * 65535)

    def increase_brightness(self, step=None):
        if not step:
            self._brightness += self.brightness_step
        else:
            self._brightness += step

        if self._brightness > 100:
            self._brightness = 100

        self.set_brightness(self._brightness, self._layer_last)

    def decrease_brightness(self, step=None):
        if not step:
            self._brightness -= self.brightness_step
        else:
            self._brightness -= step

        if self._brightness < 0:
            self._brightness = 0

        self.set_brightness(self._brightness, self._layer_last)

    def _key_led_inc(self, *args, **kwargs):
        self.increase_brightness()

    def _key_led_dec(self, *args, **kwargs):
        self.decrease_brightness()
