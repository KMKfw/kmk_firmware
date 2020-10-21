# OLED
import board

import adafruit_displayio_ssd1306
import displayio
import terminalio
from adafruit_display_text import label
from kb import KMKKeyboard
from kmk.extensions.rgb import RGB
from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.power import Power
from kmk.modules.split import Split, SplitType

keyboard = KMKKeyboard()


keyboard.tap_time = 320
keyboard.debug_enabled = False

rgb_ext = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=27, val_limit=100, hue_default=190, sat_default=100, val_default=5)

split = Split(split_type=SplitType.BLE)
power = Power(powersave_pin=keyboard.powersave_pin)
layers = Layers()

keyboard.modules = [split, power, layers]
keyboard.extensions = [rgb_ext]

enable_oled = False

if enable_oled:
    displayio.release_displays()
    i2c = board.I2C()
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
    splash = displayio.Group(max_size=10)
    display.show(splash)
else:
    displayio.release_displays()
    keyboard.i2c_deinit_count += 1

_______ = KC.TRNS
XXXXXXX = KC.NO

LT1_SP = KC.MO(2)
LT2_SP = KC.LT(3, KC.SPC)
TAB_SB = KC.LT(5, KC.TAB)
SUPER_L = KC.LM(4, KC.LGUI)

keyboard.keymap = [
    # DVORAK
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # | Esc  |   '  |   ,  |   .  |   P  |   Y  |                    |   F  |   G  |   C  |   R  |   L  | BKSP |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # | Tab  |   A  |   O  |   E  |   U  |   I  |                    |   D  |   H  |   T  |   N  |   S  |  ENT |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # | Shft |   ;  |   Q  |   J  |   K  |   X  |-------.    ,-------|   B  |   M  |   W  |   V  |   Z  |   /  |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |  Ctl |  Up  |
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'
    #
    [
        # DVORAK
        KC.GESC,  KC.QUOT, KC.COMM, KC.DOT,  KC.P,    KC.Y,                      KC.F,    KC.G,    KC.C,    KC.R,    KC.L,    KC.BSPC, \
        TAB_SB,   KC.A,    KC.O,    KC.E,    KC.U,    KC.I,                      KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.ENT, \
        KC.LSFT,  KC.SCLN, KC.Q,    KC.J,    KC.K,    KC.X,                      KC.B,    KC.M,    KC.W,    KC.V,    KC.Z,    KC.SLSH, \
                                        KC.LALT, SUPER_L, LT1_SP,   LT2_SP,  KC.LCTL, KC.N0
    ],

    # GAMING
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # | Tab  |   '  |   ,  |   .  |   P  |   Y  |                    |   F  |   G  |   C  |   R  |   L  | BKSP |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # | Ctl  |   A  |   O  |   E  |   U  |   I  |                    |   D  |   H  |   T  |   N  |   S  |  ENT |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # | Shft |   ;  |   Q  |   J  |   K  |   X  |-------.    ,-------|   B  |   M  |   W  |   V  |   Z  |   /  |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | / Space /       \LT2_SP\  |  Ctl |  Up  |
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'
    #
    [
        # GAMING
        KC.ESC,   KC.QUOT, KC.COMM, KC.DOT,  KC.P,    KC.Y,                     KC.F,    KC.G,    KC.C,    KC.R,    KC.L,    KC.BSPC, \
        KC.LCTL,  KC.A,    KC.O,    KC.E,    KC.U,    KC.I,                     KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.ENT, \
        KC.LSFT,  KC.SCLN, KC.Q,    KC.J,    KC.K,    KC.X,                     KC.B,    KC.M,    KC.W,    KC.V,    KC.Z,    KC.SLSH, \
                                            KC.LALT, KC.SPC,  KC.SPC,   LT2_SP,   KC.LCTL, KC.UP,
    ],
    # RAISE1
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # |Reprog|      |      |      |      |      |                    |      |      |   7  |  8   |  9   |      |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |      |      |      |      |      |                    |      |      |   4  |  5   |  6   |   \  |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |      |      |      |      |      |-------.    ,-------|      |      |   1  |  2   |  3   |   -  |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |   =  |  0   |
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'
    #
    [
        # RAISE1
        _______, _______, _______, _______, _______, _______,                 KC.PS_TOG, XXXXXXX, KC.N7,   KC.N8,   KC.N9,    KC.DEL,  \
        _______, _______, _______, _______, _______, _______,                   XXXXXXX, XXXXXXX, KC.N4,   KC.N5,   KC.N6,    KC.BSLS, \
        _______, _______, _______, _______, _______, _______,                   XXXXXXX, XXXXXXX, KC.N1,   KC.N2,   KC.N3,    KC.MINS, \
                                            _______, _______, _______, _______, KC.EQL,  KC.N0,
    ],
    # RAISE2
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # |      |  F9  |  F10 |  F11 |  F12 |      |                    |      |      |      |      |      | SIns |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |  F5  |  F6  |  F7  |  F8  |      |                    |      | Left | Down |  Up  |Right |      |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |  F1  |  F2  |  F3  |  F4  |      |-------.    ,-------|      |      |      |      |      |   \  |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |Dvorak|Gaming|
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'
    #

    [
        # RAISE2
        _______, KC.F9,   KC.F10,  KC.F11,  KC.F12,  _______,                     _______, _______, _______, KC.LBRC, KC.RBRC, KC.LSHIFT(KC.INS), \
        _______, KC.F5,   KC.F6,   KC.F7,   KC.F8,   _______,                     KC.HOME, KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT, KC.END,  \
        _______, KC.F1,   KC.F2,   KC.F3,   KC.F4,   _______,                     _______, _______, _______, _______, _______, KC.BSLS, \
                                            _______, _______,  _______,  _______, KC.DF(0), KC.DF(1),
    ],
    # GUI
    # ,-----------------------------------------.                    ,-----------------------------------------.
    # |      |  1   |   2  |   3  |   4  |  5   |                    |      |      |      |      |      |      |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |  6   |   7  |   8  |   9  |  0   |                    |      |      |      |      |      |      |
    # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
    # |      |      |      |      |      |      |-------.    ,-------|      |      |      |      |      |      |
    # `-----------------------------------------/       /     \      \-----------------------------------------'
    #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |      |      |
    #                          |      |      |/       /         \      \ |      |      |
    #                          `---------------------'           '------''-------------'

    [
        # GUI
        _______, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                       _______, _______, _______, _______, _______, _______, \
        _______, KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,                       _______, _______, _______, _______, _______, _______, \
        _______, _______, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______, \

                                            _______, _______,  _______, _______,  _______, _______ \
    ],
     # SYMBOLS
     # ,-----------------------------------------.                    ,-----------------------------------------.
     # |      |  !   |   @  |   #  |   $  |  %   |                    |   ^  |   &  |   *  |   (  |  )   | Del  |
     # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
     # |      |      |      |      |      |      |                    |      |      |      |   [  |  ]   |      |
     # |------+------+------+------+------+------|                    |------+------+------+------+------+------|
     # |      |      |      |      |      |      |-------.    ,-------|      |      |      |      |      |      |
     # `-----------------------------------------/       /     \      \-----------------------------------------'
     #                          | LALT | LGUI | /LT1_SP /       \LT2_SP\  |      |      |
     #                          |      |      |/       /         \      \ |      |      |
     #                          `---------------------'           '------''-------------'
     #
    [
        # SYMBOLS
        _______, KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC,                     KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL, \
        _______, KC.RGB_HUI, KC.RGB_HUD, KC.RGB_VAI, KC.RGB_VAD, _______,                     _______, _______, _______, KC.LBRC, KC.RBRC, _______, \
        _______, KC.RGB_RST, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______, \
                                            KC.RGB_TOG, _______,  _______, _______,  _______, _______,
    ]

]

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE)
