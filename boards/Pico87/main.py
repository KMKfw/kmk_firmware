import board
from kb import KMKKeyboard
from kmk.modules.layers import Layers
from kmk.extensions.lock_status import LockStatus
from kmk.keys import KC

Pico87 = KMKKeyboard()

layers = Layers()
Pico87.modules.append(layers())

locks = LockStatus()
keyboard.extensions.append(locks)

KC.CAPS.after_press_handler(toggle_caps_led)
MOLAYER = KC.MO(1)
MOLAYER.after_press_handler(led_1_on)
MOLAYER.after_release_handler(led_1_off)

Pico87.keymap = [
   
  [ # Layer 0 QWERTY
KC.ESC,   KC.NO, KC.F1, KC.F2,  KC.F3,  KC.F4, KC.NO,  KC.F5, KC.F6, KC.F7,   KC.F8,   KC.F9,    KC.F10,   KC.F11,  KC.F12, KC.PSCREEN, KC.SCROLLLOCK, KC.PAUSE,
KC.GRAVE, KC.N1, KC.N2, KC.N3,  KC.N4,  KC.N5, KC.N6,  KC.N7, KC.N8, KC.N9,   KC.N0,   KC.MINUS, KC.EQUAL, KC.NO,     KC.BSPC, KC.INS,  KC.HOME,       KC.PGUP,
KC.TAB,   KC.NO,  KC.Q,  KC.W,   KC.E,   KC.R,  KC.T,   KC.Y,  KC.U,  KC.I,    KC.O,    KC.P,     KC.LBRC,  KC.RBRC,   KC.BSLS, KC.DEL, KC.END,       KC.PGDN,
KC.CAPS,  KC.NO,    KC.A,  KC.S,   KC.D,   KC.F,  KC.G,   KC.H,  KC.J,  KC.K,    KC.L,    KC.SCLN,  KC.QUOT,  KC.ENT,    KC.NO, KC.NO,      KC.NO,      KC.NO,
KC.NO,    KC.LSHIFT, KC.Z,  KC.X,   KC.C,   KC.V,  KC.B,   KC.N,  KC.M,  KC.COMM, KC.DOT,  KC.SLSH,  KC.NO,    KC.RSHIFT, KC.NO,    KC.NO,   KC.UP,   KC.NO,
KC.LCTL,  KC.LGUI,   KC.NO, KC.LALT, KC.NO, KC.NO, KC.SPC, KC.NO, KC.NO, KC.NO,   KC.RALT, KC.RGUI,  KC.NO,    MOLAYER,     KC.RCTRL, KC.LEFT, KC.DOWN, KC.RIGHT,
  ],
  
    [# Layer 1
KC.ESC,   KC.NO, KC.F1, KC.F2,  KC.F3,  KC.F4, KC.NO,  KC.F5, KC.F6, KC.F7,   KC.F8,   KC.F9,    KC.F10,   KC.F11,  KC.F12, KC.PSCREEN, KC.SCROLLLOCK, KC.PAUSE,
KC.GRAVE, KC.N1, KC.N2, KC.N3,  KC.N4,  KC.N5, KC.N6,  KC.N7, KC.N8, KC.N9,   KC.N0,   KC.MINUS, KC.EQUAL, KC.NO,     KC.BSPC, KC.INS,  KC.HOME,       KC.PGUP,
KC.TAB,   KC.NO,  KC.Q,  KC.W,   KC.E,   KC.R,  KC.T,   KC.Y,  KC.U,  KC.I,    KC.O,    KC.P,     KC.LBRC,  KC.RBRC,   KC.BSLS, KC.DEL, KC.END,       KC.PGDN,
KC.CAPS,  KC.NO,    KC.A,  KC.S,   KC.D,   KC.F,  KC.G,   KC.H,  KC.J,  KC.K,    KC.L,    KC.SCLN,  KC.QUOT,  KC.ENT,    KC.NO, KC.NO,      KC.NO,      KC.NO,
KC.NO,    KC.LSHIFT, KC.Z,  KC.X,   KC.C,   KC.V,  KC.B,   KC.N,  KC.M,  KC.COMM, KC.DOT,  KC.SLSH,  KC.NO,    KC.RSHIFT, KC.NO,    KC.NO,   KC.UP,   KC.NO,
KC.LCTL,  KC.LGUI,   KC.NO, KC.LALT, KC.NO, KC.NO, KC.SPC, KC.NO, KC.NO, KC.NO,   KC.RALT, KC.RGUI,  KC.NO,    MOLAYER,     KC.RCTRL, KC.LEFT, KC.DOWN, KC.RIGHT,
  ],
]

def toggle_caps_led(key, keyboard, *args):
   if locks.get_caps_lock():
      Pico87.leds.set_brightness(100, leds=[0])
    else:
      Pico87.leds.set_brightness(0, leds=[0])
   
 def led_1_on:
   Pico87.leds.set_brightness(100, leds=[1])

 def led_1_off:
   Pico87.leds.set_brightness(0, leds=[1])


if __name__ == '__main__':
    Pico87.go()
