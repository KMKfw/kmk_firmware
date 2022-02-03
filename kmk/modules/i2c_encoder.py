# See docs/i2c_encoder.md for how to use
# Build to support Adafruit I2C QT Rotary Encoder with NeoPixel 
# https://www.adafruit.com/product/4991

from adafruit_seesaw import seesaw, neopixel, rotaryio, digitalio
from supervisor import ticks_ms

import traceback

from kmk.modules import Module

class Encoder:

    VELOCITY_MODE = False # not really for detents

    def __init__(self, i2c, address, is_inverted=False):
        self.seesaw = seesaw.Seesaw(i2c, address)

        # Check for correct product
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        if seesaw_product != 4991:
            print("Wrong firmware loaded?  Expected 4991")

        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)

        self.seesaw.pin_mode(24, self.seesaw.INPUT_PULLUP)
        self.switch = digitalio.DigitalIO(self.seesaw, 24)
        self.pixel = neopixel.NeoPixel(self.seesaw, 6, 1)

        self.is_inverted = is_inverted

        self._state = self.encoder.position
        self._direction = None
        self._pos = 0
        self._button_state = True
        self._button_held = False
        self._velocity = 0

        self._movement = 0
        self._timestamp = ticks_ms()

        # callback functions on events. Need to be defined externally
        self.on_move_do = None
        self.on_button_do = None

    def get_state(self):
        return {
            'direction': self.is_inverted and -self._direction or self._direction,
            'position': self._state,
            'is_pressed': not self.switch.value,
            'is_held': self._button_held,
            # 'velocity': self._velocity,
        }

    # Called in a loop to refresh encoder state
    def update_state(self):

        # Rotation events
        new_state = self.encoder.position
        if new_state != self._state:
            # it moves !
            self._movement += 1
            # false / false and true / true are common half steps
            # looking on the step just before helps determining
            # the direction
            if self.encoder.position > self._state:
                self._direction = 1
            else:
                self._direction = -1
            self._state = new_state
            self.on_move_do(self.get_state())

        # Velocity
        if self.VELOCITY_MODE:
            new_timestamp = ticks_ms()
            self._velocity = new_timestamp - self._timestamp
            self._timestamp = new_timestamp

        # Button events
        if not self.switch.value and not self._button_held:
            # Pressed
            self._button_held = True
            if self.on_button_do is not None:
                self.on_button_do(self.get_state())

        if self.switch.value and self._button_held:
            self._button_held = False
            # Released

    # returnd knob velocity as milliseconds between position changes (detents)
    # for backwards compatibility
    def vel_report(self):
        return self._velocity

class EncoderHandler(Module):
    def __init__(self):
        self.encoders = []
        self.i2c = None
        self.map = None

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        if self.i2c and self.map:
            for idx, definition in enumerate(self.i2c):
                new_encoder = Encoder(*definition)
                # In our case, we need to define keybord and encoder_id for callbacks
                new_encoder.on_move_do = lambda x, bound_idx = idx: self.on_move_do(keyboard, bound_idx, x)
                new_encoder.on_button_do = lambda x, bound_idx = idx: self.on_button_do(keyboard, bound_idx, x)
                self.encoders.append(new_encoder)
        return

    def on_move_do(self, keyboard, encoder_id, state):

        if self.map:
            layer_id = keyboard.active_layers[0]
            # if Left, key index 0 else key index 1
            if state['direction'] == -1:
                key_index = 0
            else:
                key_index = 1
            key = self.map[layer_id][encoder_id][key_index]
            keyboard.tap_key(key)

    def on_button_do(self, keyboard, encoder_id, state):
        if state['is_pressed'] is True:
            layer_id = keyboard.active_layers[0]
            key = self.map[layer_id][encoder_id][2]
            keyboard.tap_key(key)

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        for encoder in self.encoders:
            encoder.update_state()

        return keyboard

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
