from kb import KMKKeyboard
from kmk.modules.split import Split
from kmk.modules.layers import Layers
from kmk.modules.holdtap import HoldTap
from kmk.extensions.rgb import RGB
from kmk.extensions.peg_oled_display import Oled,OledDisplayMode,OledReactionType,OledData
from kmk.extensions.media_keys import MediaKeys

from kmk.keys import KC

keyboard = KMKKeyboard()
keyboard.debug_enabled = True

# Adding modules
split = Split(
    # split_target_left=True,
    split_flip=False,
    use_pio=True
)

combo_layers = { (1, 2): 3 }
layers = Layers(combo_layers)

keyboard.modules = [split, layers, HoldTap()]

# Adding extensions
rgb = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=34, hue_default=128, sat_default=255, val_default=128)
oled_ext = Oled(
    OledData(
        corner_one={0:OledReactionType.STATIC,1:["layer"]},
        corner_two={0:OledReactionType.LAYER,1:["1","2","3","4"]},
        corner_three={0:OledReactionType.LAYER,1:["base","raise","lower","adjust"]},
        corner_four={0:OledReactionType.LAYER,1:["qwerty","sym","nav","leds"]}
        ),
        toDisplay=OledDisplayMode.TXT,flip=False)
keyboard.extensions = [rgb, oled_ext, MediaKeys()]

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

ENTER = KC.HT(KC.ENT, KC.LCTRL)
LOWER = KC.MO(1)
BSPC = KC.LT(2, KC.BSPC)
ADJUST = KC.MO(3)

# Symbols
LPAR = KC.LSFT(KC.N9)
RPAR = KC.LSFT(KC.N0)
LGT = KC.LSFT(KC.COMM)
RGT = KC.LSFT(KC.DOT)
PIPE = KC.LSFT(KC.BSLS)
AMP = KC.LSFT(KC.N7)

# Media/Nav/Other
MENU = KC.LGUI(KC.F12)

# RGB
RGB1 = KC.RGB_M_P
RGB2 = KC.RGB_M_B
RGB3 = KC.RGB_M_R
RGB4 = KC.RGB_M_BR
RGB5 = KC.RGB_M_K
RGB6 = KC.RGB_M_S
RGBTOG = KC.RGB_TOG

keyboard.keymap = [
     [  #QWERTY
        KC.ESC,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                          KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.TILD,\
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                           KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.MINS,\
        KC.LCTL, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                           KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,\
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.LBRC,      KC.RBRC, KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT,\
                                   KC.LGUI, KC.LALT, ENTER,   LOWER,        BSPC,    KC.SPC,  KC.LALT, ADJUST,
    ],
    [   #LOWER
        XXXXXXX, KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,                          KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11, \
        XXXXXXX, XXXXXXX, XXXXXXX, LPAR,    RPAR,    KC.PLUS,                        XXXXXXX, KC.KP_7, KC.KP_8, KC.KP_9, XXXXXXX, KC.F12, \
        _______, XXXXXXX, XXXXXXX, KC.LBRC, KC.RBRC, KC.EQL,                         XXXXXXX, KC.KP_4, KC.KP_5, KC.KP_6, XXXXXXX, XXXXXXX,\
        _______, XXXXXXX, XXXXXXX, LGT,     RGT,     PIPE,    AMP,          XXXXXXX, KC.KP_0, KC.KP_1, KC.KP_2, KC.KP_3, KC.BSLS, XXXXXXX,\
                                   _______, _______, _______, _______,      _______, _______, _______, _______,
    ],
    [   #UPPER
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                        MENU,    XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,\
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                        KC.VOLU, KC.HOME, KC.UP,   KC.END,  KC.PGUP, XXXXXXX,\
        _______, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                        KC.VOLD, KC.LEFT, KC.DOWN, KC.RGHT, KC.PGDN, XXXXXXX,\
        _______, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,      KC.MNXT, KC.MPLY, KC.INS,  KC.DEL,  XXXXXXX, XXXXXXX, XXXXXXX,\
                                   _______, _______, _______, _______,      _______, _______, _______, _______,
    ],
    [   #ADJUST
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                        RGB1,    RGB2,    RGB3,    RGB4,    RGB5,    RGB6,   \
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,\
        _______, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,\
        _______, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,      XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, RGBTOG, \
                                   _______, _______, _______, _______,      _______, _______, _______, _______,
    ]
]

if __name__ == '__main__':
    keyboard.go()