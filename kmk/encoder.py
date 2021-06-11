import digitalio
from .kmktime import ticks_ms


class Encoder:
    def __init__(
        self,
        pad_a,
        pad_b,
        button_pin=None,
        is_inverted=False,
        increment_key=None,
        decrement_key=None,
        vel_mode=False,
        use_map = False
    ):
        self.pad_a = self.PreparePin(pad_a)  # board pin for enc pin a
        self.pad_b = self.PreparePin(pad_b)  # board pin for enc pin b
        self.button_pin = self.PreparePin(button_pin)  # board pin for enc btn
        self.button_state = None  # state of pushbutton on encoder if enabled
        self.encoder_value = 0   # clarify what this value is
        self.encoder_state = "00"  # quaderature encoder state
        self.encoder_direction = None  # arbitrary, tells direction of knob
        self.last_encoder_state = None  # not used yet
        self.resolution = 2  # number of keys sent per position change
        self.revolution_count = 20  # position changes per revolution
        self.has_button = False  # enable/disable button functionality
        self.encoder_data = None  # 6tuple containing all encoder data
        self.position_change = None  # revolution count, inc/dec as knob turns
        self.last_encoder_value = 0  # not used
        self.is_inverted = is_inverted  # switch to invert knob direction
        self.increment_key = increment_key  # list of increment keys
        self.decrement_key = decrement_key  # list of decrement keys
        self.vel_mode = vel_mode  # enable the velocity ouput
        self.vel_ts = None  # velocity timestamp
        self.last_vel_ts = 0  # last velocity timestamp
        self.debug = False  # do not spew debug info by default
        self.encoder_speed = None  # ms per position change(4 states)
        self.use_map = use_map

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
        encoder_pad_a = int(self.pad_a.value)
        encoder_pad_b = int(self.pad_b.value)
        new_encoder_state = "{}{}".format(encoder_pad_a, encoder_pad_b)

        if self.encoder_state == "11":  # Resting position
            if new_encoder_state == "10":  # Turned right 1
                self.encoder_direction = "R"
            elif new_encoder_state == "01":  # Turned left 1
                self.encoder_direction = "L"
        elif self.encoder_state == "10":  # R1 or L3 position
            if new_encoder_state == "00":  # Turned right 1
                self.encoder_direction = "R"
            elif new_encoder_state == "11":  # Turned left 1
                if self.encoder_direction == "L":
                    self.encoder_value = self.encoder_value - 1
        elif self.encoder_state == "01":  # R3 or L1
            if new_encoder_state == "00":  # Turned left 1
                self.encoder_direction = "L"
            elif new_encoder_state == "11":  # Turned right 1
                if self.encoder_direction == "R":
                    self.encoder_value = self.encoder_value + 1
        else:  # self.encoder_state == '11'
            if new_encoder_state == "10":  # Turned left 1
                self.encoder_direction = "L"
            elif new_encoder_state == "01":  # Turned right 1
                self.encoder_direction = "R"
            elif (
                new_encoder_state == "11"
            ):  # Skipped intermediate 01 or 10 state, however turn completed
                if self.encoder_direction == "L":
                    self.encoder_value = self.encoder_value - 1
                elif self.encoder_direction == "R":
                    self.encoder_value = self.encoder_value + 1

        self.encoder_state = new_encoder_state

        if self.vel_mode:
            self.vel_ts = ticks_ms()


        if self.encoder_state != self.last_encoder_state:
            self.position_change = self.invert_rotation(
                self.encoder_value, self.last_encoder_value
            )

            self.encoder_data = (
                self.encoder_state,
                self.encoder_direction,
                self.encoder_value,
                self.position_change,
                self.encoder_speed,
                self.button_state
            )
            if self.debug:
                print(
                    'State: {}, \
                    Direction: {}, \
                    Value: {}, \
                    Rev Count: {}, \
                    Speed: {}" \
                    Button State: {}'.format(
                        self.encoder_data[0],
                        self.encoder_data[1],
                        self.encoder_data[2],
                        self.encoder_data[3],
                        self.encoder_data[4],
                        self.encoder_data[5]
                    )
                )
            self.last_encoder_state = self.encoder_state
            self.last_encoder_value = self.encoder_value

            if self.position_change > 0:
                #return self.increment_key
                return 0
            elif self.position_change < 0:
                #return self.decrement_key
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
