import board

from kb_kb2040 import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys

keyboard = KMKKeyboard()
keyboard.tap_time = 150
keyboard.debug_enabled = False

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

# Adding extensions
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels, val_limit=50, hue_default=190, sat_default=100, val_default=5)

holdtap = HoldTap()
layers = Layers()
media_keys = MediaKeys()

encoder_handler = EncoderHandler()

keyboard.modules = [layers, holdtap]  #, encoder_handler]
keyboard.modules.append(MouseKeys())
keyboard.extensions = [rgb, media_keys]


encoder_handler.pins = ((board.D3, board.D2, board.D10, False))

ZOOM_IN = KC.LCTRL(KC.EQUAL)
ZOOM_OUT = KC.LCTRL(KC.MINUS)

LYR_BASE, LYR_NAV, LYR_SYM, LYR_SNAV, LYR_MEDIA, LYR_MOUSE = 0, 1, 2, 3, 4, 5

NAV_ENT = KC.LT(LYR_NAV, KC.ENT)
SYM_SPC = KC.LT(LYR_SYM, KC.SPC)
SNAV_TAB = KC.LT(LYR_SNAV, KC.TAB)
MEDIA_BSPC = KC.LT(LYR_MEDIA, KC.BSPC)
MOUSE_M = KC.LT(LYR_MOUSE, KC.M)

# HOMEROW MODS
LCTL_A = KC.HT(KC.A, KC.LCTRL)
LGUI_R = KC.HT(KC.R, KC.LGUI)
LALT_S = KC.HT(KC.S, KC.LALT)
LSFT_T = KC.HT(KC.T, KC.LSFT)
RSFT_N = KC.HT(KC.N, KC.RSFT)
RALT_E = KC.HT(KC.E, KC.RALT)
RGUI_I = KC.HT(KC.I, KC.RGUI)
RCTL_O = KC.HT(KC.O, KC.RCTRL)

# OTHER SHORTCUTS
BRWSR_LFT = KC.LCTRL(KC.LSFT(KC.TAB))
BRWSR_RGHT = KC.LCTRL(KC.TAB)
DESK_LEFT = KC.LCTRL(KC.LGUI(KC.LEFT))
DESK_RIGHT = KC.LCTRL(KC.LGUI(KC.RIGHT))
CAPSWORD = _______  # TODO: IMPLEMENT THIS

# SHIFT NAV
SFT_PGUP = KC.LSFT(KC.PGUP)
SFT_PGDN = KC.LSFT(KC.PGDN)
SFT_HOME = KC.LSFT(KC.HOME)
SFT_END = KC.LSFT(KC.END)
SFT_UP = KC.LSFT(KC.UP)
SFT_DOWN = KC.LSFT(KC.DOWN)
SFT_LEFT = KC.LSFT(KC.LEFT)
SFT_RGHT = KC.LSFT(KC.RIGHT)

RGB_TOG = KC.RGB_TOG
RGB_HUI = KC.RGB_HUI
RGB_HUD = KC.RGB_HUI
RGB_SAI = KC.RGB_SAI
RGB_SAD = KC.RGB_SAD
RGB_VAI = KC.RGB_VAI
RGB_VAD = KC.RGB_VAD
RGB_ANI = KC.RGB_ANI
RGB_AND = KC.RGB_AND
RGB_M_P = KC.RGB_MODE_PLAIN
RGB_M_B = KC.RGB_MODE_BREATHE
RGB_M_R = KC.RGB_MODE_RAINBOW
RGB_M_BR = KC.RGB_MODE_BREATHE_RAINBOW
RGB_M_K = KC.RGB_MODE_KNIGHT
RGB_M_S = KC.RGB_MODE_SWIRL

keyboard.keymap = [
    [  #COLEMAK-DH
        KC.ESC,    KC.Q,    KC.W,    KC.F,    KC.P,    KC.B,                          KC.J,       KC.L,    KC.U,     KC.Y,   KC.SCLN, KC.BSPC,
        KC.CAPS,   LCTL_A,  LGUI_R,  LALT_S,  LSFT_T,  KC.G,          KC.MUTE,        MOUSE_M,    RSFT_N,  RALT_E,   RGUI_I, RCTL_O,  KC.QUOT,
        KC.SPC,    KC.Z,    KC.X,    KC.C,    KC.D,    KC.V,                          KC.K,       KC.H,    KC.COMM,  KC.DOT, KC.SLSH, KC.RSFT,
                            KC.MUTE, KC.DEL,  NAV_ENT, SNAV_TAB,                      MEDIA_BSPC, SYM_SPC, KC.QUOT,  KC.LCTRL(KC.BSPC)
    ],
    [  #NAVIGATION
        _______,     KC.ESC,      KC.PGUP,     KC.UP,       KC.PGDN,     _______,             KC.ASTR,     KC.N7,     KC.N8,       KC.N9,     KC.PLUS,     _______,
        _______,     KC.HOME,     KC.LEFT,     KC.DOWN,     KC.RIGHT,    KC.END,   _______,   KC.SLSH,     KC.N4,     KC.N5,       KC.N6,     KC.MINS,     _______,
        _______,     _______,     _______,     _______,     _______,     _______,             KC.EQL,      KC.N1,     KC.N2,       KC.N3,     KC.N0,       _______,
                                  _______,     _______,     _______,     _______,             KC.BKSP,     KC.SPC,    KC.DOT,      _______,
    ],
    [  #SYMBOLS
        _______,     KC.EXLM,     KC.AT,       KC.HASH,     KC.DLR,      KC.PERC,             KC.CIRC,     KC.AMPR,     KC.ASTR,     KC.UNDS,     KC.EQL,      _______,
        _______,     KC.MINS,     KC.LBRC,     KC.LCBR,     KC.LPRN,     KC.LABK,  _______,   KC.RABK,     KC.RPRN,     KC.RCBR,     KC.RBRC,     KC.PLUS,     _______,
        _______,     KC.CAPS,     KC.GRV,      BRWSR_LFT,   DESK_LEFT,   CAPSWORD,            _______,     DESK_RIGHT,  BRWSR_RGHT,  _______,     KC.BSLS,     _______,
                                  _______,     _______,     KC.ENT,      KC.TAB,              _______,     _______,     _______,     _______,
    ],
    [  #SHIFT NAVIGATION
        _______,     _______,     SFT_PGUP,    SFT_UP,      SFT_PGDN,    _______,             _______,     _______,     _______,     _______,     _______,     _______,
        _______,     SFT_HOME,    SFT_LEFT,    SFT_DOWN,    SFT_RGHT,    SFT_END,  _______,   KC.VOLU,     KC.MPLY,     KC.MSTP,     _______,     _______,     _______,
        _______,     _______,     _______,     _______,     _______,     KC.MUTE,             KC.VOLD,     KC.MPRV,     KC.MNXT,     _______,     _______,     _______,
                                  _______,     _______,     _______,     _______,             _______,     _______,     _______,     _______,
    ],
    [  #MEDIA
        _______,     RGB_TOG,     _______,     _______,     _______,     _______,             _______,     _______,     _______,     _______,     _______,     _______,
        _______,     _______,     RGB_HUI,     RGB_SAI,     RGB_VAI,     RGB_ANI,  _______,   RGB_M_P,     RGB_M_B,     RGB_M_R,     RGB_M_BR,    RGB_M_K,     _______,
        _______,     _______,     RGB_HUD,     RGB_SAD,     RGB_VAD,     RGB_AND,             RGB_M_S,     _______,     _______,     _______,     _______,     _______,
                                  _______,     _______,     _______,     _______,             _______,     _______,     _______,     _______,
    ],
    [  #MOUSE
        _______,     KC.RESET,    KC.MW_UP,    KC.MS_UP,    KC.MW_DN,    _______,             _______,     _______,     _______,     _______,     _______,     _______,
        _______,     _______,     KC.MS_LT,    KC.MS_DN,    KC.MS_RT,    _______,  _______,   _______,     _______,     _______,     _______,     _______,     _______,
        _______,     _______,     _______,     _______,     _______,     _______,             _______,     _______,     _______,     _______,     _______,     _______,
                                  _______,     _______,     _______,     _______,             _______,     _______,     _______,     _______,
    ],
]

encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.MUTE)),  # Layer 1
    ((ZOOM_OUT, ZOOM_IN, _______)),  # Layer 2
    ((_______, _______, _______)),  # Layer 3
    ((_______, _______, _______)),  # Layer 4
    ((_______, _______, _______)),  # Layer 5
    ((_______, _______, _______)),  # Layer 6
]

if __name__ == '__main__':
    keyboard.go()
