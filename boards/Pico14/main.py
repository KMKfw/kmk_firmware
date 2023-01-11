from kb import KMKKeyboard

from kmk.extensions.LED import LED
from kmk.extensions.lock_status import LockStatus
from kmk.keys import KC
from kmk.modules.layers import Layers

Pico14 = KMKKeyboard()


class LEDLockStatus(LockStatus):
    def __init__(self, leds):
        super().__init__()
        self._leds = leds

    def set_lock_leds(self):
        if self.get_num_lock():
            self._leds.set_brightness(100, leds=[0])
        else:
            self._leds.set_brightness(0, leds=[0])

    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Removing this will break lock status.

        if self.report_updated:
            self.set_lock_leds()


Pico14.modules.append(Layers())
leds = LED(led_pin=[Pico14.led_pin], val=0)
Pico14.extensions.append(leds)
Pico14.extensions.append(LEDLockStatus(leds))

# Make this for better looking formatting...
______ = KC.TRNS
XXXXXX = KC.NO

Pico14.keymap = [[
  # Layer 0 QWERTY
    KC.NUMLOCK,  KC.NUMPAD_SLASH, KC.NUMPAD_ASTERISK,
    KC.NUMPAD_7, KC.NUMPAD_8,     KC.NUMPAD_9,
    KC.NUMPAD_4, KC.NUMPAD_5,     KC.NUMPAD_6,
    KC.NUMPAD_1, KC.NUMPAD_2,     KC.NUMPAD_1,
    KC.NUMPAD_0, XXXXXX,          KC.NUMPAD_DOT
  ], [
  # Layer 1
    ______,      ______,          ______,
    KC.HOME,     KC.UP,           KC.PGUP,
    KC.LEFT,     ______,          KC.RIGHT,
    KC.END,      KC.DOWN,         KC.PGDN,
    KC.INS,      XXXXXX,          KC.DEL
  ]
]

if __name__ == '__main__':
    Pico14.go()
