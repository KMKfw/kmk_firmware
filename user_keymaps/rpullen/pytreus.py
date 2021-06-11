import gc

from kmk.boards.teensy_41.pytreus import KMKKeyboard
from kmk.consts import LeaderMode, UnicodeMode
from kmk.handlers.sequences import compile_unicode_string_sequences as cuss
from kmk.handlers.sequences import send_string
from kmk.keys import KC, make_key

import board



local_increment = None
local_decrement = None

keyboard = KMKKeyboard()
keyboard.tap_time = 250
keyboard.debug_enabled = False

# custom keys used for encoder actions
Zoom_in = KC.LCTRL(KC.EQUAL)
Zoom_out = KC.LCTRL(KC.MINUS)

# standard filler keys
_______ = KC.TRNS
XXXXXXX = KC.NO
CAD = KC.LCTL(KC.LALT(KC.DEL))
RES = KC.LCTL(KC.LSFT(KC.ESC))
FE = KC.LGUI(KC.E)
LT1_DEL = KC.LT(1,KC.DEL)
LT2_ENT = KC.LT(2, KC.ENT)

# programming layer keys
INT = send_string('int')
UINT = send_string('uint')
DOUBLE = send_string('double')
BOOL = send_string('bool')
BYTE = send_string('byte')
SBYTE = send_string('sbyte')
CHAR = send_string('char')
GETSET = send_string('{get; set; }')
PUBLIC = send_string('public ')

# tapdance config
#MODE_TD = KC.TD(
    #KC.MO(1),
    #KC.MO(2),
#)

PRINT = send_string('print(')
DEBUGWL = send_string('Debug.WriteLine(')


#### begin oled config ####
keyboard.enable_oleds = True
keyboard.oled_scl = [board.SCL]
keyboard.oled_sda = [board.SDA]
keyboard.oled_width = [128]
keyboard.oled_height = [32]
keyboard.oled_count = len(keyboard.oled_width)
keyboard.make_oleds()
#### end oled config ####


#********************** begin single board encoder setup *******************************
# use this for non-split boards, adding more action keys adds more encoders

# The encoders will populate based on several setup lists, all of the list must have the same amount of items
#
keyboard.enable_encoder = True
keyboard.enc_a  =    [board.D40] # list of pad a pins
keyboard.enc_b  =    [board.D41] # list of pad b pins
keyboard.encoder_count = 1 # len(keyboard.enc_a) # number of encoders based off of pad length, or use int

# encoder map follows state layering just like the key map
# the encoder map is a list of lists like the keymap and
# contains 3 item tuples in the format of (increment key, decrement key, resolution).
# the encoder map should have the same amount of layers as the keymap, usenoop codes when you want
# to sicence the encoder. The amount of tuples should match the number of physical encoders present
keyboard.encoder_map = [
    [
        (KC.VOLU,KC.VOLD,2),# Only 1 encoder is being used, so only one tuple per layer is required
    ],
    [
        (Zoom_in, Zoom_out,1),
    ],
    [
        (_______,_______,1), # no action taken by the encoder on this layer
    ]
]

# initiate the encoder list
keyboard.make_encoders()
#********************** end single board encoder setup *********************************



# below is the depricated encoder constructor, left here as notes for now.
# #********************** begin split board encoder setup ********************************
# # handle keycode setup for split boards using the same MCU pins for encoders
# # use this only for split keyboards
# keyboard.enable_encoder = True
# if keyboard.is_target:
#     local_increment = [KC.VOLU]
#     local_decrement = [KC.VOLD]
# elif not keyboard.is_target:
#     local_increment = [Zoom_in]
#     local_decrement = [Zoom_out]


# # begin encoder birthing
# keyboard.enc_a = [board.D31] # list of pad a pins
# keyboard.enc_b = [board.D32] # list of pad b pins
# keyboard.encoder_resolution = [4] # list of encoder resolutions
# keyboard.increment_keys = local_increment # list of increment key codes
# keyboard.decrement_keys = local_decrement # list of decrement key codes
# keyboard.encoder_count = len(keyboard.enc_a) # number of encoders based off of pad length
# # initiate the encoder list
# keyboard.make_encoders()
# #********************** end split board encoder setup **********************************


# make keymap
keyboard.keymap = [
    [
        KC.ESC,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,       KC.N6,     KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS,
        KC.CAPS,      KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,        KC.Y,      KC.U,    KC.I,    KC.O,    KC.P,    KC.BSLS,
        KC.TAB,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,        KC.H,      KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        CAD,  KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,        KC.N,      KC.M,    KC.COMM, KC.DOT,  KC.SLSH,  FE,
        KC.BSPC,  KC.DEL, KC.LALT, KC.LSFT, KC.LCTL,  KC.BSPC,     KC.SPC,    KC.ENT,  KC.LSFT, KC.RCTL, KC.ENT,  KC.RGUI,
        XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.MO(1),    KC.MO(2),  KC.MUTE, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    ],
    [
        RES,      XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,     KC.PSLS, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.MINS,
        KC.BSLS,  XXXXXXX, XXXXXXX, KC.UP,   XXXXXXX, XXXXXXX,     KC.PAST, KC.N7,   KC.N8,   KC.N9,   XXXXXXX, KC.BSLS,
        KC.TAB,   XXXXXXX, KC.LEFT, KC.DOWN, KC.RIGHT,KC.HASH,     KC.PPLS, KC.N4,   KC.N5,   KC.N6,   XXXXXXX, KC.QUOT,
        KC.LSFT,  XXXXXXX, XXXXXXX, KC.C,    KC.TAB,  KC.UNDS,     KC.MINS, KC.N1,   KC.N2,   KC.N3,   XXXXXXX, KC.LBRC,
        KC.BSPC,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, _______,     KC.SPC,  KC.EQUAL,  KC.N0, KC.DOT, KC.ENT,  KC.RGUI,
        XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, _______,     _______, _______,   XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    ],
    [
        RES,      KC.N1,   KC.N2,   KC.N3,   KC.N4,      KC.N5,      DEBUGWL,    PRINT,   KC.N8,   KC.N9,   KC.N0,   KC.MINS,
        KC.BSLS,  KC.Q,    KC.W,    KC.LCBR, KC.RCBR,    KC.AT,      INT,     PUBLIC,    GETSET,    KC.O,    KC.P,    KC.BSLS,
        KC.TAB,   KC.A,    KC.S,    KC.LPRN, KC.RPRN,    KC.DLR,     BOOL,     DOUBLE,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        KC.LSFT,  KC.Z,    KC.X,    KC.LBRC, KC.RBRC,    KC.PERC,    UINT ,     BYTE,    KC.COMM, KC.DOT,  KC.SLSH, KC.LBRC,
        KC.BSPC,  KC.LGUI, KC.LALT, KC.LSFT, KC.LCTL,    KC.DEL,     _______,  KC.EQL,  KC.RCTL, KC.RALT, KC.ENT,  KC.RGUI,
        XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,   _______,     _______, _______,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
    ]
]


if __name__ == "__main__":
    keyboard.go()
