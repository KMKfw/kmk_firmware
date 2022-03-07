from kmk.modules import Module
import rotaryio


class RotaryIOEncoder(Module):
    """This class enables the use of rotary encoders.
    It is a pretty thin wrapper around rotaryio.IncrementalEncoder.
    WARNING: The two pins used for the encoder must be adjacent (e.g.
             GP16 and GP17 on a Pi pico)
    """

    def __init__(self, pin_a, pin_b, divisor=4):
        self.encoder = rotaryio.IncrementalEncoder(pin_a,pin_b,divisor)
        self.old_position = self.encoder.position
        self.change = None
        self.map = None

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''

        self.change = self.encoder.position - self.old_position

        if self.change != 0:
            layer_id = keyboard.active_layers[0]
            key = self.map[layer_id][1 if self.change > 0 else 0]
            keyboard.tap_key(key)

        self.old_position = self.encoder.position

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
