# from board import LED_B, LED_R, LED_G
import is31fl3733
from kb import KMKKeyboard

from kmk.hid import HIDModes
from kmk.extensions.media_keys import MediaKeys
import kmk.extensions.rgb
# from kmk.extensions.statusled import statusLED
from kmk.modules.mouse_keys import MouseKeys
# from kmk.modules.power import Power
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
keyboard.debug_enabled = False
keyboard.modules = [Layers(), MouseKeys()]

pixels = is31fl3733.Helper(63)
pixels.brightness = 0.2
rgb = kmk.extensions.rgb.RGB(pixel_pin=None, num_pixels=len(pixels), pixels=pixels, animation_mode=kmk.extensions.rgb.AnimationModes.RAINBOW, disable_auto_write=0)
keyboard.extensions = [MediaKeys(),rgb]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

BASE = 0
FN1 = 1


keyboard.keymap = [
    [
        KC.ESC, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS, KC.EQL,  KC.BSPC,
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC, KC.RBRC, KC.BSLS,
        KC.CAPS, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,           KC.ENT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH,                   KC.RSFT,
        KC.LCTL, KC.LALT, KC.LGUI,                       KC.SPC,                     KC.RALT, KC.APP, KC.MO(FN1), KC.RCTL,
    ],
    [
        KC.GRAVE,    KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.DEL,
        KC.RGB_TOG, KC.RGB_MODE_SWIRL, KC.UP,   KC.RGB_MODE_RAINBOW,   KC.RESET, _______, _______, _______, _______, _______, _______, KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP, KC.AUDIO_MUTE,
        _______, KC.LEFT, KC.DOWN, KC.RGHT, _______, _______, KC.MS_LEFT, KC.MS_DOWN, KC.MS_UP, KC.MS_RIGHT, KC.BRIGHTNESS_DOWN, KC.BRIGHTNESS_UP, _______,
        _______, _______, _______, _______, _______, KC.BOOTLOADER, _______, _______, KC.MEDIA_PREV_TRACK, KC.MEDIA_NEXT_TRACK, KC.MEDIA_PLAY_PAUSE, _______,
        KC.GRV, _______, _______, _______, _______,          _______, _______, _______,
    ],
]

print("Battery:",keyboard.battery_level())

if keyboard.is_usb_connected():
    print("USB mode...")
    keyboard.go(hid_type=HIDModes.USB)
else:
    keyboard.battery_power_on()
    print("Bluetooth mode...")
    keyboard.go(hid_type=HIDModes.BLE, ble_name='M60 Keyboard')