from kb import KMKKeyboard

from kmk.extensions.international import International
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap

# Layers must be imported after HoldTap
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(International())
keyboard.modules.append(HoldTap())

combo_layers = {
    (1, 2): 3,  # ADJUST
}
keyboard.modules.append(Layers(combo_layers))

LOWER = KC.MO(1)
RAISE = KC.MO(2)

RGB_VAI = KC.TRNS
RGB_VAD = KC.TRNS
RGB_SAI = KC.TRNS
RGB_SAD = KC.TRNS
RGB_HUI = KC.TRNS
RGB_HUD = KC.TRNS
RGB_ANI = KC.TRNS
RGB_AND = KC.TRNS
RGB_TOG = KC.TRNS

if keyboard.has_underglow is True:
    from kmk.extensions.rgb import RGB, AnimationModes

    keyboard.extensions.append(
        RGB(
            pixel_pin=keyboard.underglow_pin,
            num_pixels=keyboard.underglow_led_number,
            val_limit=keyboard.underglow_max_brightness,
            hue_default=0,
            sat_default=255,
            val_default=128,
            animation_speed=1,
            animation_mode=AnimationModes.BREATHING_RAINBOW,
            breathe_center=1,  # 1.0 - 2.7
            knight_effect_length=4,
        )
    )

    RGB_VAI = KC.RGB_VAI
    RGB_VAD = KC.RGB_VAD
    RGB_SAI = KC.RGB_SAI
    RGB_SAD = KC.RGB_SAD
    RGB_HUI = KC.RGB_HUI
    RGB_HUD = KC.RGB_HUD
    RGB_ANI = KC.RGB_ANI
    RGB_AND = KC.RGB_AND
    RGB_TOG = KC.RGB_TOG


# fmt: off
keyboard.keymap = [
    [  #BASE
        KC.GRV,   KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                        KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,     KC.BSPC,
        KC.TAB,   KC.Q,     KC.W,     KC.E,     KC.R,     KC.T,                         KC.Y,     KC.U,     KC.I,     KC.O,     KC.P,      KC.DEL,
        KC.LCTL,  KC.A,     KC.S,     KC.D,     KC.F,     KC.G,        KC.MUTE,         KC.H,     KC.J,     KC.K,     KC.L,     KC.SCLN,   KC.QUOT,
        KC.LSFT,  KC.Z,     KC.X,     KC.C,     KC.V,     KC.B,                         KC.N,     KC.M,     KC.COMM,  KC.DOT,   KC.SLSH,   KC.RSFT,
                                      KC.LGUI,  KC.LALT,  LOWER,    KC.SPC,   KC.SPC,   RAISE,    KC.RALT,  KC.RGUI,
    ],
    [  #LOWER
        KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,                        KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,     KC.NO,
        KC.NO,    KC.EXLM,  KC.AT,    KC.HASH,  KC.DLR,   KC.PERC,                      KC.CIRC,  KC.AMPR,  KC.ASTR,  KC.LPRN,  KC.RPRN,   KC.DEL,
        KC.NO,    KC.F1,    KC.F2,    KC.F3,    KC.F4,    KC.F5,         KC.NO,         KC.F6,    KC.UNDS,  KC.PLUS,  KC.LCBR,  KC.RCBR,   KC.PIPE,
        KC.NO,    KC.F7,    KC.F8,    KC.F9,    KC.F10,   KC.F11,                       KC.F12,   KC.NUHS,  KC.NUBS,  KC.HOME,  KC.END,    KC.RSFT,
                                      KC.NO,    KC.NO,    KC.TRNS,  KC.NO,    KC.TRNS,  KC.TRNS,  KC.NO,    KC.NO,
    ],
    [  #RAISE
        KC.NO,    KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                        KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,     KC.DEL,
        KC.NO,    KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                        KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,     KC.DEL,
        KC.NO,    KC.MINS,  KC.EQL,   KC.LBRC,  KC.RBRC,  KC.BSLS,       KC.NO,         KC.F1,    KC.F2,    KC.F3,    KC.F4,    KC.F5,     KC.F6,
        KC.NO,    KC.ESC,   KC.RGUI,  KC.RALT,  KC.CAPS,  KC.QUOT,                      KC.F7,    KC.F8,    KC.F9,    KC.F10,   KC.F11,    KC.F12,
                                      KC.NO,    KC.NO,    KC.TRNS,  KC.BSPC,  KC.TRNS,  KC.NO,    KC.NO,    KC.NO,
    ],
    [  #ADJUST
        KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,                        KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,     KC.NO,
        RGB_VAI,  RGB_SAI,  RGB_HUI,  RGB_ANI,  KC.NO,    RGB_TOG,                      KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,     KC.NO,
        RGB_VAD,  RGB_SAD,  RGB_HUD,  RGB_AND,  KC.NO,    KC.NO,         KC.NO,         KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,     KC.NO,
        KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,                        KC.RESET, KC.NO,    KC.NO,    KC.NO,    KC.NO,     KC.NO,
                                      KC.NO,    KC.NO,    KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.TRNS,  KC.NO,    KC.NO,
    ],
]
# fmt: on

if __name__ == '__main__':
    keyboard.go()
