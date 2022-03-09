import rotaryio

from kmk.modules import Module


class RotaryIOEncoder(Module):
    """This class enables the use of rotary encoders.
    It is a pretty thin wrapper around rotaryio.IncrementalEncoder.
    WARNING: The two pins used for the encoder must be adjacent (e.g.
             GP16 and GP17 on a Pi pico)

    Does not support buttons, they should be part of the keyboard matrix
    """

    def __init__(self,encoders):
        """self.encoders is a list of dictionaries, with keys
         "encoder": rotaryio.IncrementalEncoder objext
         "keymap": tuple of pairs (one per layer) with the keymap
         "pin_a":
         "pin_b":
         "divisor":
        self.encoders
        """

	self.encoders = encoders

        for enc in self.encoders:
            # if you didn't give it explicitly you probably want divisor = 4
            enc["divisor"] = enc.get("divisor",4)
            enc["encoder"] = rotaryio.IncrementalEncoder(
                                        enc["pin_a"],
                                        enc["pin_b"],
                                        enc["divisor"])

            enc["old_position"] = enc["encoder"].position

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''

        for enc in self.encoders:

            change = enc["encoder"].position - enc["old_position"]

            if change != 0:
                layer_id = keyboard.active_layers[0]
                key = enc["keymap"][layer_id][1 if change > 0 else 0]
                keyboard.tap_key(key)

            enc["old_position"] = enc["encoder"].position

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
