from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers

# fmt: off
# --8<-- [start:config]
# ↓ EDIT CONFIG HERE ↓
splaytoraid_keys = 40       # Options: 36, 40
splaytoraid_rgb = False     # Options: False, True
# ↑ EDIT CONFIG HERE ↑
# --8<-- [end:config]
# fmt: on

keyboard = KMKKeyboard(splaytoraid_keys, splaytoraid_rgb)

keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

# Enable debugging: https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/debugging.md
# keyboard.debug_enabled = True


# Key aliases
xxxxxxx = KC.NO
_______ = KC.TRNS
RAISE = KC.MO(1)

# Keymap
# fmt: off
keyboard.keymap = [
    [
       # BASE
       #         |          |          |          |          |         -|          |-         |          |          |          |          |          |          |
           KC.TAB,      KC.Q,      KC.W,      KC.E,      KC.R,      KC.T,                 KC.Y,      KC.U,      KC.I,      KC.O,      KC.P,   KC.BSPC,
          KC.LCTL,      KC.A,      KC.S,      KC.D,      KC.F,      KC.G,                 KC.H,      KC.J,      KC.K,      KC.L,   KC.SCLN,   KC.QUOT,
                        KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,                 KC.N,      KC.M,   KC.COMM,    KC.DOT,   KC.SLSH,
                                           KC.LSFT,    KC.ESC,    KC.ENT,   KC.MPLY,    KC.SPC,    KC.DEL,     RAISE,
    ],
    [
       # RAISE
       #         |          |          |          |          |         -|          |-         |          |          |          |          |          |          |
            KC.N1,     KC.N2,     KC.N3,     KC.N4,     KC.N4,     KC.N5,                KC.N6,     KC.N7,     KC.N8,     KC.N9,     KC.N0,   KC.MINS,
          KC.LCTL,      KC.A,      KC.S,      KC.D,      KC.F,      KC.G,                 KC.H,      KC.J,      KC.K,      KC.L,   KC.SCLN,   KC.QUOT,
                        KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,                 KC.N,      KC.M,   KC.COMM,    KC.DOT,   KC.SLSH,
                                           KC.LSFT,    KC.ESC,    KC.ENT,   KC.MPLY,    KC.SPC,    KC.DEL,   _______,
    ],

]
# fmt: on


# Encoder
encoder_handler = EncoderHandler()
encoder_handler.pins = ((keyboard.encoder_a, keyboard.encoder_b, None),)
# Encoder keymap
encoder_handler.map = (
    ((KC.VOLU, KC.VOLD),),  # Encoder function on BASE layer
    ((KC.MNXT, KC.MPRV),),  # Encoder function on RAISE layer
)
keyboard.modules.append(encoder_handler)


if __name__ == '__main__':
    keyboard.go()
