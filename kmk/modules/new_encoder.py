# How to use this module in your main / code file
#
# 1. load the module
# from kmk.modules.new_encoder import EncoderHandler
# encoder_handler = EncoderHandler()
# keyboard.modules = [layers, modtap, encoder_handler]
#
# 2. Define the pins for each encoder (pin_a, pin_b, pin_button, True for an inversed encoder)
# encoder_handler.pins = ((board.GP17, board.GP15, board.GP14, False), (encoder 2 definition), etc. )
#
# 3. Define the mapping of keys to be called (1 / layer)
# encoder_handler.map = [(( KC.A, KC.Z, KC.E),(encoder 2 mapping), (etc.)), # Layer 1
#                        ((KC.A, KC.Z, KC.N1),(encoder 2 mapping), (etc.)), # Layer 2
#                        ((KC.A, KC.Z, KC.N1),(encoder 2 mapping), (etc.)), # Layer 3
#                        ((KC.A, KC.Z, KC.N1),(encoder 2 mapping), (etc.)), # Layer 4
#                        ]
# 4. Encoder methods on_move_do and on_button_do can be overwritten for complex use cases
#

import digitalio

from kmk.kmktime import tick_ms
from kmk.modules import Module

# NB : not using rotaryio as it requires the pins to be consecutive


class Encoder:

    VELOCITY_MODE = True
    STATES = {
        # old_pos_a, old_pos_b, new_pos_a, new_pos_b
        # -1 : Left ; 1 : Right ; 0 : we don't care
        ((True, True), (True, False)): -1,
        ((True, True), (False, True)): 1,
        ((True, False), (False, False)): -1,
        ((True, False), (True, True)): 0,
        ((False, True), (False, False)): 1,
        ((False, True), (True, True)): 0,
        ((False, False), (True, False)): 0,
        ((False, False), (False, True)): 0,
        ((False, False), (True, True)): 0,
        ((False, True), (True, False)): 0,
        ((True, False), (False, True)): 0,
        ((True, True), (False, False)): 0,
    }

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
        self._timestamp = tick_ms()

        # callback functions on events. Need to be defined externally
        self.on_move_do = None
        self.on_button_do = None

    def get_state(self):
        return {
            'direction': self.is_inverted
            and -self._direction
            or self._direction,
            'position': self.is_inverted and -self._pos or self._pos,
            'is_pressed': not self._button_state,
            'velocity': self.velocity
        }

    # Called in a loop to refresh encoder state
    def update_state(self):
        # Rotation events
        new_state = (self.pin_a.get_value(), self.pin_b.get_value())
        if new_state != self._state:
            self._movement += 1
            new_direction = self.STATES[(self._state, new_state)]
            if new_direction != 0:
                self._direction = new_direction

            # when the encoder settles on a position (every 2 steps)
            if (
                new_state == (True, True) and self._movement > 2
            ):  # if < 2 state changes, it is a misstep
                self._movement = 0
                self._pos += self._direction
                if self.on_move_do is not None:
                    self.on_move_do(self.get_state())

            self._state = new_state

        # Velocity
        if VELOCITY_MODE:
            new_timestamp = tick_ms()
            self._velocity = new_timestamp - self._timestamp
            self._timestamp = new_timestamp

        # Button events
        new_button_state = self.pin_button.get_value()
        if new_button_state != self._button_state:
            self._button_state = new_button_state
            if self.on_button_do is not None:
                self.on_button_do(self.get_state())

    # returnd knob velocity as milliseconds between position changes (detents)
    def vel_report(self):
        return self._velocity

    # callback for actions on move (set up externally)
    def on_move_do(self, :
        return

    # callback for actions on button press (set up externally)
    def on_button_do:
        return


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
