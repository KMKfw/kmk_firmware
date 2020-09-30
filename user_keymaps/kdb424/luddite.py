from kmk.boards.converter.fourtypercentclub.luddite import KMKKeyboard
from kmk.keys import KC

keyboard = KMKKeyboard()

# ---------------------------------- Config  --------------------------------------------

keyboard.tap_time = 150

keyboard.rgb_config['num_pixels'] = 16
keyboard.rgb_config['val_limit'] = 150
keyboard.rgb_config['hue_step'] = 10
keyboard.rgb_config['sat_step'] = 5
keyboard.rgb_config['val_step'] = 5
keyboard.rgb_config['hue_default'] = 260
keyboard.rgb_config['sat_default'] = 100
keyboard.rgb_config['val_default'] = 0
keyboard.rgb_config['knight_effect_length'] = 6
keyboard.rgb_config['animation_mode'] = 'static'
keyboard.rgb_config['animation_speed'] = 2
keyboard.debug_enabled = False


# ---------------------- Custom Functions --------------------------------------------

BASE = 0
GAMING = 1
FN1 = 2

_______ = KC.TRNS
XXXXXXX = KC.NO
HOME = KC.MT(KC.HOME, KC.LSFT)
END = KC.MT(KC.END, KC.RSFT)
LEFT_LAY = KC.LT(FN1, KC.LEFT)
SHFT_INS = KC.LSFT(KC.INS)
SPC = KC.LT(2, KC.SPC)


# ---------------------- Keymap ---------------------------------------------------------


keyboard.keymap = [
    # df
    [
        KC.GESC, KC.N1,   KC.N2,   KC.N3,  KC.N4,   KC.N5,   KC.N6,   KC.N7, KC.N8, KC.N9, KC.N0, KC.LBRC, KC.RBRC, KC.BSPC,
        KC.LEAD, KC.QUOT, KC.COMM, KC.DOT, KC.P,    KC.Y,    KC.F,    KC.G,  KC.C,  KC.R,  KC.L,  KC.SLSH, KC.EQL,  KC.BSLS,
        KC.TAB,  KC.A,    KC.O,    KC.E,   KC.U,    KC.I,    KC.D,    KC.H,  KC.T,  KC.N,  KC.S,  KC.MINS, KC.ENT,
        KC.LSFT, KC.SCLN, KC.Q,    KC.J,   KC.K,    KC.X,    KC.B,    KC.M,  KC.W,  KC.V,  KC.Z,  KC.RSFT,
        KC.LCTL, KC.LGUI, KC.LALT,           SPC,              KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT,
    ],

    # df
    [
        KC.GESC, KC.N1,   KC.N2,   KC.N3,  KC.N4,   KC.N5,   KC.N6,   KC.N7, KC.N8, KC.N9, KC.N0, KC.LBRC, KC.RBRC, KC.BSPC,
        KC.LEAD, KC.QUOT, KC.COMM, KC.DOT, KC.P,    KC.Y,    KC.F,    KC.G,  KC.C,  KC.R,  KC.L,  KC.SLSH, KC.EQL,  KC.BSLS,
        KC.TAB,  KC.A,    KC.O,    KC.E,   KC.U,    KC.I,    KC.D,    KC.H,  KC.T,  KC.N,  KC.S,  KC.MINS, KC.ENT,
        KC.LSFT, KC.SCLN, KC.Q,    KC.J,   KC.K,    KC.X,    KC.B,    KC.M,  KC.W,  KC.V,  KC.Z,  KC.RSFT,
        KC.LCTL, KC.LGUI, KC.LALT,        KC.SPC,              LEFT_LAY, KC.DOWN, KC.UP,   KC.RIGHT,
    ],

    # fn
    [
        KC.GESC, KC.F1,      KC.F2,      KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7, KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.DEL,
        KC.RESET, KC.RGB_HUD, KC.RGB_HUI, _______, _______, _______, _______, _______, _______, KC.RGB_M_S, _______, _______, KC.VOLU, SHFT_INS,
        _______,   KC.RGB_SAD, KC.RGB_SAI, _______, _______, _______, _______, _______, KC.RGB_TOG, _______, KC.RGB_M_P, KC.VOLD, _______,
        _______,    KC.RGB_VAD, KC.RGB_VAI, _______, _______, _______, _______, _______,    _______,    _______,    _______, _______,
        _______, _______,    _______,    _______, _______, _______, KC.DF(0),     KC.DF(1),
    ],
]

if __name__ == '__main__':
    keyboard.go()
