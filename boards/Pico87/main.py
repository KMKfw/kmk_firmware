import board

from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.extensions.lock_status import LockStatus
from kmk.extensions.stringy_keymaps import StringyKeymaps

Pico87 = KMKKeyboard()

Pico87.modules.append(Layers())

locks = LockStatus()
Pico87.extensions.append(locks)
Pico87.extensions.append(StringyKeymaps())


def toggle_caps_led(key, keyboard, *args):
    if locks.get_caps_lock():
        Pico87.leds.set_brightness(100, leds=[0])
    else:
        Pico87.leds.set_brightness(0, leds=[0])


def led_1_on():
    Pico87.leds.set_brightness(100, leds=[1])


def led_1_off():
    Pico87.leds.set_brightness(0, leds=[1])

# toggle_caps_led()
# led_1_off()

KC.CAPS.after_release_handler(toggle_caps_led)
MOLYR = KC.MO(1)
# MOLAYER.after_press_handler(led_1_on)
# MOLAYER.after_release_handler(led_1_off)

# Make this for better looking formatting...
______ = 'NO'

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

if __name__ == '__main__':
    Pico87.go()
