from kmk.common.pins import PULL_UP


class RotaryEncoder:
    # Please don't ask. I don't know. All I know is bit_value
    # works as expected. Here be dragons, etc. etc.
    MIN_VALUE = False + 1 << 1 | True + 1
    MAX_VALUE = True + 1 << 1 | True + 1

    def __init__(self, pos_pin, neg_pin):
        self.pos_pin = pos_pin
        self.neg_pin = neg_pin

        self.pos_pin.switch_to_input(pull=PULL_UP)
        self.neg_pin.switch_to_input(pull=PULL_UP)

        self.prev_bit_value = self.bit_value()

    def value(self):
        return (self.pos_pin.value(), self.neg_pin.value())

    def bit_value(self):
        '''
        Returns 2, 3, 5, or 6 based on the state of the rotary encoder's two
        bits. This is a total hack but it does what we need pretty efficiently.
        Shrug.
        '''
        return self.pos_pin.value() + 1 << 1 | self.neg_pin.value() + 1

    def direction(self):
        '''
        Compares the current rotary position against the last seen position.

        Returns True if we're rotating "positively", False if we're rotating "negatively",
        and None if no change could safely be detected for any reason (usually this
        means the encoder itself did not change)
        '''
        new_value = self.bit_value()
        rolling_under = self.prev_bit_value == self.MIN_VALUE and new_value == self.MAX_VALUE
        rolling_over = self.prev_bit_value == self.MAX_VALUE and new_value == self.MIN_VALUE
        increasing = new_value > self.prev_bit_value
        decreasing = new_value < self.prev_bit_value
        self.prev_bit_value = new_value

        if rolling_over:
            return True
        elif rolling_under:
            return False

        if increasing:
            return True
        if decreasing:
            return False

        # Either no change, or not a type of change we can safely detect,
        # so safely do nothing
        return None
