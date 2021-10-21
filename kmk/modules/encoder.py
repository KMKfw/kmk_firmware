# See docs/encoder.md for how to use

import digitalio
from supervisor import ticks_ms

from kmk.modules import Module

# NB : not using rotaryio as it requires the pins to be consecutive


class Encoder:

    VELOCITY_MODE = True

    def __init__(self, pin_a, pin_b, pin_button=None, is_inverted=False):
        self.pin_a = EncoderPin(pin_a)
        self.pin_b = EncoderPin(pin_b)
        self.pin_button = EncoderPin(pin_button, button_type=True)
        self.is_inverted = is_inverted

        self._state = (self.pin_a.get_value(), self.pin_b.get_value())
        self._direction = None
        self._pos = 0
        self._button_state = True
        self._velocity = 0

        self._movement = 0
        self._timestamp = ticks_ms()

        # callback functions on events. Need to be defined externally
        self.on_move_do = None
        self.on_button_do = None

    def get_state(self):
        return {
            'direction': self.is_inverted and -self._direction or self._direction,
            'position': self.is_inverted and -self._pos or self._pos,
            'is_pressed': not self._button_state,
            'velocity': self._velocity,
        }

    # Called in a loop to refresh encoder state
    def update_state(self):
        # Rotation events
        new_state = (self.pin_a.get_value(), self.pin_b.get_value())

        if new_state != self._state:
            # it moves !
            self._movement += 1
            # false / false and true / true are common half steps
            # looking on the step just before helps determining
            # the direction
            if new_state[0] == new_state[1] and self._state[0] != self._state[1]:
                if new_state[1] == self._state[0]:
                    self._direction = 1
                else:
                    self._direction = -1

            # when the encoder settles on a position (every 2 steps)
            if new_state == (True, True):
                if self._movement > 2:
                    # 1 full step is 4 movements, however, when rotated quickly,
                    # some steps may be missed. This makes it behaves more
                    # naturally
                    real_movement = round(self._movement / 4)
                    self._pos += self._direction * real_movement
                    if self.on_move_do is not None:
                        for i in range(real_movement):
                            self.on_move_do(self.get_state())
                # Reinit to properly identify new movement
                self._movement = 0
                self._direction = 0

            self._state = new_state

        # Velocity
        if self.VELOCITY_MODE:
            new_timestamp = ticks_ms()
            self._velocity = new_timestamp - self._timestamp
            self._timestamp = new_timestamp

        # Button events
        new_button_state = self.pin_button.get_value()
        if new_button_state != self._button_state:
            self._button_state = new_button_state
            if self.on_button_do is not None:
                self.on_button_do(self.get_state())

    # returnd knob velocity as milliseconds between position changes (detents)
    # for backwards compatibility
    def vel_report(self):
        print(self._velocity)
        return self._velocity


class EncoderPin:
    def __init__(self, pin, button_type=False):
        self.pin = pin
        self.button_type = button_type
        self.prepare_pin()

    def prepare_pin(self):
        if self.pin is not None:
            self.io = digitalio.DigitalInOut(self.pin)
            self.io.direction = digitalio.Direction.INPUT
            self.io.pull = digitalio.Pull.UP
        else:
            self.io = None

    def get_value(self):
        return self.io.value


class EncoderHandler(Module):
    def __init__(self):
        self.encoders = []
        self.pins = None
        self.map = None

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        if self.pins and self.map:
            for idx, pins in enumerate(self.pins):
                gpio_pins = pins[:3]
                new_encoder = Encoder(*gpio_pins)
                # In our case, we need to define keybord and encoder_id for callbacks
                new_encoder.on_move_do = lambda x: self.on_move_do(keyboard, idx, x)
                new_encoder.on_button_do = lambda x: self.on_button_do(keyboard, idx, x)
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
