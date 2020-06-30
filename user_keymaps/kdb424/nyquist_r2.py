from kmk.boards.converter.keebio.nyquist_r2 import KMKKeyboard
from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.keys import KC

keyboard = KMKKeyboard()

# ------------------User level config variables ---------------------------------------
keyboard.tap_time = 150
keyboard.leader_timeout = 2000
keyboard.debug_enabled = False

# RGB Config (underglow)
keyboard.rgb_config['num_pixels'] = 12
keyboard.rgb_config['val_limit'] = 150
keyboard.rgb_config['hue_step'] = 10
keyboard.rgb_config['sat_step'] = 5
keyboard.rgb_config['val_step'] = 5
keyboard.rgb_config['hue_default'] = 260
keyboard.rgb_config['sat_default'] = 100
keyboard.rgb_config['val_default'] = 40
keyboard.rgb_config['knight_effect_length'] = 4
keyboard.rgb_config['animation_mode'] = 'static'
keyboard.rgb_config['animation_speed'] = 1
keyboard.debug_enabled = False

_______ = KC.TRNS
XXXXXXX = KC.NO
SHFT_INS = KC.LSHIFT(KC.INS)
TAB_UP = KC.RCTRL(KC.PGUP)
TAB_DOWN = KC.RCTRL(KC.PGDN)

BASE = KC.DF(0)
LT2_SP = KC.LT(3, KC.SPC)
GAMING = KC.DF(1)

HACHEEJ = simple_key_sequence((
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.J, KC.A, KC.I, KC.L, KC.N1, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.J, KC.A, KC.I, KC.L, KC.N2, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.J, KC.A, KC.I, KC.L, KC.N3, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.ENT),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.J, KC.A, KC.I, KC.L, KC.N4, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.J, KC.A, KC.I, KC.L, KC.N5, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.J, KC.A, KC.I, KC.L, KC.N6, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.ENT),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.J, KC.A, KC.I, KC.L, KC.N7, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.J, KC.A, KC.I, KC.L, KC.N8, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.J, KC.A, KC.I, KC.L, KC.N9, KC.LSFT(KC.SCOLON),
        KC.ENT
        ))

HACHEEF = simple_key_sequence((
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.N1, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.N2, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.N3, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.ENT),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.N4, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.N5, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.N6, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.ENT),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.N7, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.N8, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.H, KC.A, KC.C, KC.H, KC.E, KC.E, KC.N9, KC.LSFT(KC.SCOLON),
        KC.ENT
        ))

THIGHS = simple_key_sequence((
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N1, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N2, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N3, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N4, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.ENT),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N5, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N6, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N7, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N8, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.ENT),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N9, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N1, KC.N0, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N1, KC.N1, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N1, KC.N2, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.ENT),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N1, KC.N3, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N1, KC.N4, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N1, KC.N5, KC.LSFT(KC.SCOLON),
        KC.LSFT(KC.SCOLON), KC.T, KC.H, KC.I, KC.G, KC.H, KC.S, KC.N1, KC.N6, KC.LSFT(KC.SCOLON),
        KC.ENT
        ))

# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    [
        # df
        KC.GESC,  KC.N1,    KC.N2,    KC.N3,   KC.N4,   KC.N5,  KC.N6,  KC.N7,     KC.N8,   KC.N9,   KC.N0, KC.DEL,
        KC.GRV,   KC.QUOTE, KC.COMMA, KC.DOT,  KC.P,    KC.Y,   KC.F,   KC.G,      KC.C,    KC.R,    KC.L,  KC.BKSP,
        KC.TAB,   KC.A,     KC.O,     KC.E,    KC.U,    KC.I,   KC.D,   KC.H,      KC.T,    KC.N,    KC.S,  KC.ENT,
        KC.LSFT,  KC.SCLN,  KC.Q,     KC.J,    KC.K,    KC.X,   KC.B,   KC.M,      KC.W,    KC.V,    KC.Z,  KC.SLSH,
        KC.LCTRL, KC.LGUI,  KC.LALT,  KC.RGB_TOG, KC.MO(2), LT2_SP, KC.SPC, KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT,
    ],
    [
        # gw
        KC.GESC,  KC.N1,   KC.N2,   KC.N3,  KC.N4, KC.N5,  KC.N6,  KC.N7,     KC.N8,   KC.N9,   KC.N0, KC.DEL,
        KC.TAB,   KC.QUOT, KC.COMM, KC.DOT, KC.P,  KC.Y,   KC.F,   KC.G,      KC.C,    KC.R,    KC.L,  KC.BKSP,
        KC.ESC,   KC.A,    KC.O,    KC.E,   KC.U,  KC.I,   KC.D,   KC.H,      KC.T,    KC.N,    KC.S,  KC.ENT,
        KC.LSFT,  KC.SCLN, KC.Q,    KC.J,   KC.K,  KC.X,   KC.B,   KC.M,      KC.W,    KC.V,    KC.Z,  KC.SLSH,
        KC.LCTRL, KC.LGUI, KC.LALT, KC.F1,  KC.F2, KC.SPC, LT2_SP, KC.MO(4), KC.LEFT, KC.DOWN, KC.UP, KC.RIGHT,
    ],
    [
        # r1
        KC.GESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL,
        KC.TILD,  KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL,
        _______,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.LBRC, KC.RBRC, KC.BSLS,
        _______,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.INS,  _______, _______, KC.MINS,
        KC.RESET, _______, _______, _______, _______, _______, _______, KC.EQL,  KC.HOME, KC.PGDN, KC.PGUP, KC.END,
    ],
    [
        # r2
        KC.GESC, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8, KC.N9, KC.N0,   KC.DEL,
        _______, _______, _______, _______, _______, _______, HACHEEF, THIGHS, KC.N7, KC.N8, KC.N9,   KC.BKSP,
        _______, _______, _______, _______, _______, _______, _______, HACHEEJ,  KC.N4, KC.N5, KC.N6,   XXXXXXX,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.N1, KC.N2, KC.N3,   XXXXXXX,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.N0, KC.N0, KC.PDOT, KC.ENT,
    ],
    [
        # r3
        KC.GESC,    KC.RGB_M_P, KC.RGB_M_K, KC.RGB_M_B, KC.RGB_M_BR, KC.RGB_M_S, _______, _______, KC.F10,  KC.F11,  KC.F12,  KC.DEL,
        KC.RGB_ANI, KC.RGB_HUD, KC.RGB_HUI, _______,    _______,     _______,    _______, _______, KC.F7,   KC.F8,   KC.F9,   SHFT_INS,
        KC.RGB_AND, KC.RGB_SAD, KC.RGB_SAI, _______,    _______,     _______,    _______, _______, KC.F4,   KC.F5,   KC.F6,   TAB_UP,
        _______,    KC.RGB_VAD, KC.RGB_VAI, _______,    _______,     _______,    _______, _______, KC.F1,   KC.F2,   KC.F4,   TAB_DOWN,
        BASE,       GAMING,     _______,    _______,    _______,     _______,    _______, _______, _______, _______, _______, XXXXXXX,
    ],
]

if __name__ == '__main__':
    keyboard.go()
