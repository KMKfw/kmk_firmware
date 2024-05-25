from kb import KMKKeyboard

from kmk.extensions.lock_status import LockStatus
from kmk.extensions.stringy_keymaps import StringyKeymaps
from kmk.keys import KC
from kmk.modules.layers import Layers

Pico87 = KMKKeyboard()


class LEDLockStatus(LockStatus):
    def set_lock_leds(self):
        if self.get_caps_lock():
            Pico87.leds.set_brightness(50, leds=[0])
        else:
            Pico87.leds.set_brightness(0, leds=[0])

        if self.get_scroll_lock():
            Pico87.leds.set_brightness(50, leds=[1])
        else:
            Pico87.leds.set_brightness(0, leds=[1])

    def after_hid_send(self, sandbox):
        # Critically important. Removing this will break lock status.
        super().after_hid_send(sandbox)

        if self.report_updated:
            self.set_lock_leds()


Pico87.modules.append(Layers())
Pico87.extensions.append(LEDLockStatus())
Pico87.extensions.append(StringyKeymaps())

MOLYR = KC.MO(1)

# Make this for better looking formatting...
______ = 'NO'

# fmt:off
Pico87.keymap = [[
  # Layer 0 QWERTY
    'ESC', ______,   'F1',   'F2',   'F3',   'F4', ______,   'F5',   'F6',   'F7',   'F8',   'F9',  'F10',  'F11',  'F12', 'PSCR', 'SLCK', 'PAUS',
    'GRV',   'N1',   'N2',   'N3',   'N4',   'N5',   'N6',   'N7',   'N8',   'N9',   'N0', 'MINS',  'EQL', ______, 'BSPC',  'INS', 'HOME', 'PGUP',
    'TAB', ______,    'Q',    'W',    'E',    'R',    'T',    'Y',    'U',    'I',    'O',    'P', 'LBRC', 'RBRC', 'BSLS',  'DEL',  'END', 'PGDN',
   'CAPS', ______,    'A',    'S',    'D',    'F',    'G',    'H',    'J',    'K',    'L', 'SCLN', 'QUOT',  'ENT', ______, ______, ______, ______,
   ______, 'LSFT',    'Z',    'X',    'C',    'V',    'B',    'N',    'M', 'COMM',  'DOT', 'SLSH', ______, 'RSFT', ______, ______,   'UP', ______,
   'LCTL', 'LGUI', ______, 'LALT', ______, ______,  'SPC', ______, ______, ______, 'RALT', 'RGUI', ______,  MOLYR, 'RCTL', 'LEFT', 'DOWN', 'RGHT',
], [
  # Layer 1
    'ESC', ______,   'F1',   'F2',   'F3',   'F4', ______,   'F5',   'F6',   'F7',   'F8',   'F9',  'F10',  'F11',  'F12', 'PSCR', 'SLCK', 'PAUS',
    'GRV',   'N1',   'N2',   'N3',   'N4',   'N5',   'N6',   'N7',   'N8',   'N9',   'N0', 'MINS',  'EQL', ______, 'BSPC',  'INS', 'HOME', 'PGUP',
    'TAB', ______,    'Q',    'W',    'E',    'R',    'T',    'Y',    'U',    'I',    'O',    'P', 'LBRC', 'RBRC', 'BSLS',  'DEL',  'END', 'PGDN',
   'CAPS', ______,    'A',    'S',    'D',    'F',    'G',    'H',    'J',    'K',    'L', 'SCLN', 'QUOT',  'ENT', ______, ______, ______, ______,
   ______, 'LSFT',    'Z',    'X',    'C',    'V',    'B',    'N',    'M', 'COMM',  'DOT', 'SLSH', ______, 'RSFT', ______, ______,   'UP', ______,
   'LCTL', 'LGUI', ______, 'LALT', ______, ______,  'SPC', ______, ______, ______, 'RALT', 'RGUI', ______,  MOLYR, 'RCTL', 'LEFT', 'DOWN', 'RGHT',
]]
# fmt:on

if __name__ == '__main__':
    Pico87.go()
