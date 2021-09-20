import digitalio
from supervisor import ticks_ms

from kmk.modules import Module


class EncoderPadState:
    OFF = False
    ON = True


class EndcoderDirection:
    Left = False
    Right = True


class Encoder:
    def __init__(
        self,
        pad_a,
        pad_b,
        button_pin=None,
    ):
        self.pad_a = self.PreparePin(pad_a)  # board pin for enc pin a
        self.pad_a_state = False
        self.pad_b = self.PreparePin(pad_b)  # board pin for enc pin b
        self.pad_b_state = False
        self.button_pin = self.PreparePin(button_pin)  # board pin for enc btn
        self.button_state = None  # state of pushbutton on encoder if enabled
        self.encoder_value = 0  # clarify what this value is
        self.encoder_state = (
            self.pad_a_state,
            self.pad_b_state,
        )  # quaderature encoder state
        self.encoder_direction = None  # arbitrary, tells direction of knob
        self.last_encoder_state = None  # not used yet
        self.resolution = 2  # number of keys sent per position change
        self.revolution_count = 20  # position changes per revolution
        self.has_button = False  # enable/disable button functionality
        self.encoder_data = None  # 6tuple containing all encoder data
        self.position_change = None  # revolution count, inc/dec as knob turns
        self.last_encoder_value = 0  # not used
        self.is_inverted = False  # switch to invert knob direction
        self.vel_mode = False  # enable the velocity output
        self.vel_ts = None  # velocity timestamp
        self.last_vel_ts = 0  # last velocity timestamp
        self.encoder_speed = None  # ms per position change(4 states)
        self.encoder_map = None
        self.eps = EncoderPadState()
        self.encoder_pad_lookup = {
            False: self.eps.OFF,
            True: self.eps.ON,
        }
        self.edr = EndcoderDirection()  # lookup for current encoder direction
        self.encoder_dir_lookup = {
            False: self.edr.Left,
            True: self.edr.Right,
        }

    def __repr__(self, idx):
        return 'ENCODER_{}({})'.format(idx, self._to_dict())

    def _to_dict(self):
        return {
            'Encoder_State': self.encoder_state,
            'Direction': self.encoder_direction,
            'Value': self.encoder_value,
            'Position_Change': self.position_change,
            'Speed': self.encoder_speed,
            'Button_State': self.button_state,
        }

    # adapted for CircuitPython from raspi
    def PreparePin(self, num):
        if num is not None:
            pad = digitalio.DigitalInOut(num)
            pad.direction = digitalio.Direction.INPUT
            pad.pull = digitalio.Pull.UP
            return pad
        else:
            return None

    # checks encoder pins, reports encoder data
    def report(self):
        new_encoder_state = (
            self.encoder_pad_lookup[int(self.pad_a.value)],
            self.encoder_pad_lookup[int(self.pad_b.value)],
        )

        if self.encoder_state == (self.eps.ON, self.eps.ON):  # Resting position
            if new_encoder_state == (self.eps.ON, self.eps.OFF):  # Turned right 1
                self.encoder_direction = self.edr.Right
            elif new_encoder_state == (self.eps.OFF, self.eps.ON):  # Turned left 1
                self.encoder_direction = self.edr.Left
        elif self.encoder_state == (self.eps.ON, self.eps.OFF):  # R1 or L3 position
            if new_encoder_state == (self.eps.OFF, self.eps.OFF):  # Turned right 1
                self.encoder_direction = self.edr.Right
            elif new_encoder_state == (self.eps.ON, self.eps.ON):  # Turned left 1
                if self.encoder_direction == self.edr.Left:
                    self.encoder_value = self.encoder_value - 1
        elif self.encoder_state == (self.eps.OFF, self.eps.ON):  # R3 or L1
            if new_encoder_state == (self.eps.OFF, self.eps.OFF):  # Turned left 1
                self.encoder_direction = self.edr.Left
            elif new_encoder_state == (self.eps.ON, self.eps.ON):  # Turned right 1
                if self.encoder_direction == self.edr.Right:
                    self.encoder_value = self.encoder_value + 1
        else:  # self.encoder_state == '11'
            if new_encoder_state == (self.eps.ON, self.eps.OFF):  # Turned left 1
                self.encoder_direction = self.edr.Left
            elif new_encoder_state == (self.eps.OFF, self.eps.ON):  # Turned right 1
                self.encoder_direction = self.edr.Right  # 'R'
            elif new_encoder_state == (
                self.eps.ON,
                self.eps.ON,
            ):  # Skipped intermediate 01 or 10 state, however turn completed
                if self.encoder_direction == self.edr.Left:
                    self.encoder_value = self.encoder_value - 1
                elif self.encoder_direction == self.edr.Right:
                    self.encoder_value = self.encoder_value + 1

        self.encoder_state = new_encoder_state

        if self.vel_mode:
            self.vel_ts = ticks_ms()

        if self.encoder_state != self.last_encoder_state:
            self.position_change = self.invert_rotation(
                self.encoder_value, self.last_encoder_value
            )

            self.last_encoder_state = self.encoder_state
            self.last_encoder_value = self.encoder_value

            if self.position_change > 0:
                self._to_dict()
                # return self.increment_key
                return 0
            elif self.position_change < 0:
                self._to_dict()
                # return self.decrement_key
                return 1
            else:
                return None

    # invert knob direction if encoder pins are soldered backwards
    def invert_rotation(self, new, old):
        if self.is_inverted:
            return -(new - old)
        else:
            return new - old

    # returns knob velocity as milliseconds between position changes(detents)
    def vel_report(self):
        self.encoder_speed = self.vel_ts - self.last_vel_ts
        self.last_vel_ts = self.vel_ts
        return self.encoder_speed


class EncoderHandler(Module):

    encoders = []
    debug_enabled = False  # not working as inttended, do not use for now

    def __init__(self, pad_a, pad_b, encoder_map):
        self.pad_a = pad_a
        self.pad_b = pad_b
        self.encoder_count = len(self.pad_a)
        self.encoder_map = encoder_map
        self.make_encoders()

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        return self.get_reports(keyboard)

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

    def make_encoders(self):
        for i in range(self.encoder_count):
            self.encoders.append(
                Encoder(
                    self.pad_a[i],  # encoder pin a
                    self.pad_b[i],  # encoder pin b
                )
            )

    def send_encoder_keys(self, keyboard, encoder_key, encoder_idx):
        # position in the encoder map tuple
        encoder_resolution = 2
        for _ in range(
            self.encoder_map[keyboard.active_layers[0]][encoder_idx][encoder_resolution]
        ):
            keyboard.tap_key(
                self.encoder_map[keyboard.active_layers[0]][encoder_idx][encoder_key]
            )
        return keyboard

    def get_reports(self, keyboard):
        for idx in range(self.encoder_count):
            if self.debug_enabled:  # not working as inttended, do not use for now
                print(self.encoders[idx].__repr__(idx))
            encoder_key = self.encoders[idx].report()
            if encoder_key is not None:
                return self.send_encoder_keys(keyboard, encoder_key, idx)
