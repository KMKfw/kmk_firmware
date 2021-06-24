from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.handlers.sequences import send_string, simple_key_sequence
import board


local_increment = None
local_decrement = None

keyboard = KMKKeyboard()

layers_ext = Layers()

keyboard.modules = [layers_ext]

keyboard.tap_time = 250
keyboard.debug_enabled = False
#keyboard.layer_names = ['BASE', 'NAV/NUM', 'PROG']
# custom keys used for encoder actions
Zoom_in = KC.LCTRL(KC.EQUAL)
Zoom_out = KC.LCTRL(KC.MINUS)

# standard filler keys
_______ = KC.TRNS
XXXXXXX = KC.NO

# custom keys
NEW = KC.LCTL(KC.N)
NEW_DIR = KC.LCTL(KC.LSFT(KC.N))
CAD = KC.LCTL(KC.LALT(KC.DEL))
RES = KC.LCTL(KC.LSFT(KC.ESC))
FE = KC.LGUI(KC.E)
LT1_DEL = KC.LT(1,KC.DEL)
LT2_ENT = KC.LT(2, KC.ENT)
SAVE_AS = KC.LCTL(KC.LSFT(KC.S))
PSCR = KC.LGUI(KC.PSCR)
SNIP = simple_key_sequence(
    (
    KC.LGUI,
    KC.MACRO_SLEEP_MS(25),
    KC.S,
    KC.N,
    KC.I,
    KC.P,
    KC.MACRO_SLEEP_MS(25),
    KC.ENT
    )
)

# programming layer keys
UINT = simple_key_sequence(
    (
        KC.U,
        KC.I,
        KC.N,
        KC.T,
    )
)
INT = simple_key_sequence(
    (
        KC.I,
        KC.N,
        KC.T,
    )
)
DOUBLE = simple_key_sequence(
    (
        KC.D,
        KC.O,
        KC.U,
        KC.B,
        KC.L,
        KC.E,
    )
)
BOOL = simple_key_sequence(
    (
        KC.B,
        KC.O,
        KC.O,
        KC.L,
    )
)
BYTE = simple_key_sequence(
    (
        KC.B,
        KC.Y,
        KC.T,
        KC.E,
    )
)
SBYTE = simple_key_sequence(
    (
        KC.S,
        KC.B,
        KC.Y,
        KC.T,
        KC.E,
    )
)
CHAR = simple_key_sequence(
    (
        KC.C,
        KC.H,
        KC.A,
        KC.R,
    )
)
GETSET = simple_key_sequence(
    (
        KC.LBRC,
        KC.SPC,
        KC.G,
        KC.E,
        KC.T,
        KC.SCLN,
        KC.SPC,
        KC.S,
        KC.E,
        KC.T,
        KC.SCLN,
        KC.SPC,
        KC.RBRC,
    )
)
PUBLIC = simple_key_sequence(
    (
        KC.P,
        KC.U,
        KC.B,
        KC.L,
        KC.I,
        KC.C,
    )
)
DEBUGWL = simple_key_sequence(
    (
        KC.LSFT(KC.D),
        KC.E,
        KC.B,
        KC.U,
        KC.G,
        KC.DOT,
        KC.LSFT(KC.W),
        KC.R,
        KC.I,
        KC.T,
        KC.E,
        KC.LSFT(KC.L),
        KC.I,
        KC.N,
        KC.E,
        KC.LSFT(KC.N9),
    )
)
PRINT = simple_key_sequence(
    (
        KC.P,
        KC.R,
        KC.I,
        KC.N,
        KC.T,
    )
)
# not workinging in current master branch
# tapdance config
# MODE_TD = KC.TD(
#     KC.MO(1),
#     KC.A,
# )

# PRINT = send_string('print(')
# DEBUGWL = send_string('Debug.WriteLine(')


# #### begin oled config ####
# keyboard.enable_oleds = True
# keyboard.oled_scl = [board.SCL]
# keyboard.oled_sda = [board.SDA]
# keyboard.oled_width = [128]
# keyboard.oled_height = [32]
# keyboard.oled_count = len(keyboard.oled_width)
# keyboard.make_oleds()
# #### end oled config ####


#********************** begin single board encoder setup *******************************
# use this for non-split boards, adding more action keys adds more encoders

# The encoders will populate based on several setup lists, all of the list must have the same amount of items
#
keyboard.enable_encoder = True
keyboard.enc_a  =    [board.D40] # list of pad a pins
keyboard.enc_b  =    [board.D41] # list of pad b pins
keyboard.encoder_count = 1 # len(keyboard.enc_a) # number of encoders based off of pad length, or use int

# initiate the encoder list
keyboard.make_encoders()

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


#********************** end single board encoder setup *********************************


# make keymap
keyboard.keymap = [
    [# qwerty
        KC.ESC,    KC.N1,     KC.N2,     KC.N3,     KC.N4,     KC.N5,          KC.N6,     KC.N7,     KC.N8,     KC.N9,     KC.N0,     KC.MINS,
        KC.CAPS,   KC.Q,      KC.W,      KC.E,      KC.R,      KC.T,           KC.Y,      KC.U,      KC.I,      KC.O,      KC.P,      KC.PSLS,
        KC.TAB,    KC.A,      KC.S,      KC.D,      KC.F,      KC.G,           KC.H,      KC.J,      KC.K,      KC.L,      KC.SCLN,   KC.QUOT,
        KC.TRNS,   KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,           KC.N,      KC.M,      KC.COMM,   KC.DOT,    KC.SLSH,   FE,
        KC.BSPC,   KC.DEL,    KC.LALT,   KC.LSFT,   KC.LCTL,   KC.BSPC,        KC.SPC,    KC.ENT,    KC.RSFT,   KC.RCTL,   KC.ENT,    KC.RGUI,
        XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   KC.MO(1),       KC.MO(2),  KC.MUTE,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,
    ],
    [  # navnum
        KC.TRNS,   SAVE_AS,   PSCR,      SNIP,      KC.LGUI,   NEW_DIR,        KC.PSLS,   KC.RGUI,   KC.NO,     KC.NO,     KC.NO,     KC.MINS,
        KC.BSLS,   KC.NO,     KC.NO,     KC.UP,     KC.NO,     NEW,            KC.N5,     KC.N6,     KC.N7,     KC.N8,     KC.N9,     KC.BSLS,
        KC.F2,     KC.NO,     KC.LEFT,   KC.DOWN,   KC.RGHT,   KC.HASH,        KC.N0,     KC.N1,     KC.N2,     KC.N3,     KC.N4,     KC.QUOT,
        KC.LSFT,   KC.NO,     KC.NO,     KC.NO,     KC.TAB,    KC.UNDS,        KC.MINS,   KC.PPLS,   KC.MINS,   KC.PAST,   KC.PSLS,   KC.LBRC,
        KC.BSPC,   KC.NO,     KC.NO,     KC.NO,     KC.NO,     KC.TRNS,        KC.SPC,    KC.EQL,    KC.N0,     KC.DOT,    KC.ENT,    KC.RGUI,
        XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   KC.TRNS,        KC.TRNS,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,
    ],
    [# sym/prog
        KC.TRNS,   KC.NO,     KC.NO,     KC.NO,     KC.F2,     KC.AMPR,        PRINT,   DEBUGWL,     SAVE_AS,   KC.NO,     KC.NO,     KC.NO,
        KC.BSLS,   KC.NO,     KC.NO,     KC.LCBR,   KC.RCBR,   KC.AT,          INT,       GETSET,    KC.UP,    KC.NO,     KC.NO,     KC.NO,
        KC.TAB,    KC.NO,     KC.NO,     KC.LPRN,   KC.RPRN,   KC.DLR,         BOOL,      KC.LEFT,    KC.DOWN,     KC.RGHT,     KC.NO,     KC.NO,
        KC.LSFT,   KC.NO,     KC.NO,     KC.LBRC,   KC.RBRC,   KC.PERC,        UINT,      DOUBLE,      KC.NO,     KC.NO,     KC.NO,     KC.NO,
        KC.BSPC,   KC.LGUI,   KC.LALT,   KC.LSFT,   KC.LCTL,   KC.DEL,         KC.TRNS,   PUBLIC,    KC.RCTL,   KC.RALT,   KC.ENT,    KC.RESET,
        XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   KC.TRNS,        KC.TRNS,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,
    ],
] 


if __name__ == "__main__":
    keyboard.go()